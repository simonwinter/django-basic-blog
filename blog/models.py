from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User

from image_cropping.fields import ImageRatioField, ImageCropField

from util import unique_slugify


class PublishedManager(models.Manager):
	def get_query_set(self):
		return super(PublishedManager, self).get_query_set().filter(status=1)

	def accessible_entries(self, user):
		return self.get_query_set().exclude(Q(visibility=1), ~Q(user=user))

class ModelWithSlug(models.Model):
	def save(self, **kwargs):
		if self.name:
			unique_slugify(self, self.name)
		elif self.title:
			unique_slugify(self, self.title)
		
		super(ModelWithSlug, self).save()

class Entry(ModelWithSlug):
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

	def save(self, **kwargs):
		unique_slugify(self, self.title)
		super(Entry, self).save()


class Category(ModelWithSlug):
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


class Tag(ModelWithSlug):
	name = models.CharField(max_length=100, help_text='Maximum of 70 characters', verbose_name='Tag Name')
	slug = models.SlugField(max_length=255)

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('blog.views.category_tag_entries', (), {'mode': 'tag', 'slug': self.slug})
