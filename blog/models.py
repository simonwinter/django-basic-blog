from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from sorl.thumbnail import ImageField


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
	
	objects = models.Manager()
	published_objects = PublishedManager()

	class Meta:
		verbose_name_plural = "Entries"
		ordering = ['-publish_date']

	def __unicode__(self):
		return self.title

	@models.permalink
	def get_absolute_url(self):
		print 'here'
		return ('blog.views.entry', (), {'slug': self.slug})
    
	def image(self):
		try:
			return EntryImage.objects.get(entry=self)
		except EntryImage.DoesNotExist:
			return None


class EntryImage(models.Model):
	entry = models.ForeignKey(Entry)
	image = ImageField(upload_to='i/uploads/%Y/%m')
	caption = models.CharField(max_length=255, blank=True)

	def __unicode__(self):
		return self.image.name


class Category(models.Model):
	name = models.CharField(max_length=100, help_text='Maximum of 70 characters', verbose_name='Category Name')
	slug = models.SlugField(max_length=255)
	can_delete = models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'

	def __unicode__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=100, help_text='Maximum of 70 characters', verbose_name='Tag Name')
	slug = models.SlugField(max_length=255)

	def __unicode__(self):
		return self.name
