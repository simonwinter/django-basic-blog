from django.db import models

from sorl.thumbnail import ImageField


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
	status = models.IntegerField(max_length=1, choices=STATUS_OPTIONS)
	visibility = models.IntegerField(max_length=1, choices=VISIBILITY_OPTIONS)

	body = models.TextField()
	excerpt = models.TextField(blank=True, help_text='A short introduction for the entry. If not supplied, \
													the first paragraph of the body will be used.')

	category = models.ForeignKey('Category')
	tags = models.ManyToManyField('Tag', blank=True)

	class Meta:
		verbose_name_plural = "Entries"

	def __unicode__(self):
		return self.title
		
	def image(self):
		try:
			return EntryImage.objects.get(entry=self)
		except:
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
