from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User

from image_cropping.fields import ImageRatioField, ImageCropField


class PublishedManager(models.Manager):
	def get_query_set(self):
		return super(PublishedManager, self).get_query_set().filter(status=1)

	def accessible_entries(self, user):
		return self.get_query_set().exclude(Q(visibility=1), ~Q(user=user))

class Entry(models.Model):
	STATUS_OPTIONS = (
						(0, 'Draft'),
						(1, 'Published'),
					)
	VISIBILITY_OPTIONS = (
							(0, 'Public'),
							(1, 'Private'),
						)

	title = models.CharField(max_length=100)
	slug = models.SlugField(max_length=255)
	publish_date = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(max_length=1, choices=STATUS_OPTIONS, default=0)
	visibility = models.IntegerField(max_length=1, choices=VISIBILITY_OPTIONS, default=0)

	body = models.TextField()
	excerpt = models.TextField(blank=True, help_text='A short introduction for the entry. If not supplied, \
													the first paragraph of the body will be used.')

	category = models.ForeignKey('Category')
	tags = models.ManyToManyField('Tag', blank=True)

	user = models.ForeignKey(User)
	
	image = ImageCropField(upload_to='i/uploads/%Y/%m')
	cropping = ImageRatioField('image', settings.IMAGE_CROPPING_SIZE)
	caption = models.CharField(max_length=255, blank=True)
	
	objects = models.Manager()
	published_objects = PublishedManager()

	class Meta:
		verbose_name_plural = "Entries"
		ordering = ['-publish_date']

	def __unicode__(self):
		return self.title

	@models.permalink
	def get_absolute_url(self):
		return ('blog.views.entry', (), {'slug': self.slug})


class Category(models.Model):
	name = models.CharField(max_length=100, help_text='Maximum of 70 characters', verbose_name='Category Name')
	slug = models.SlugField(max_length=255)
	can_delete = models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('blog.views.category_tag_entries', (), {'mode': 'category', 'slug': self.slug})


class Tag(models.Model):
	name = models.CharField(max_length=100, help_text='Maximum of 70 characters', verbose_name='Tag Name')
	slug = models.SlugField(max_length=255)

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('blog.views.category_tag_entries', (), {'mode': 'tag', 'slug': self.slug})
