from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib import messages

from tinymce.widgets import TinyMCE

from blog.models import Entry, Category, Tag
from blog.util import delete_selected_actions, thumbnail


class EntryForm(forms.ModelForm):
	body = forms.CharField(widget=TinyMCE(attrs={'cols': 85, 'rows': 30}, 
							mce_attrs={'oninit': 'entryOnInit',
										'handle_event_callback' : "entryEvent"}))
	title = forms.CharField(max_length=70, help_text='Maximum of 70 characters')

	class Meta:
		model = Entry


class EntryAdmin(admin.ModelAdmin):
	list_display = ('_thumbnail', 'title', 'category', 'author', 'publish_date', 'status', 'visibility')
	list_filter = ('category__name', 'tags__name')
	list_display_links = ('_thumbnail', 'title',)
	prepopulated_fields = {'slug': ('title',)}
	form = EntryForm

	fieldsets = (
		('Status', {
			'fields': (('status', 'visibility'), )
		}),
		('Title', {
			'fields': ('title', 'slug',)
		}),
		('Content', {
			'fields': ('excerpt', 'body',)
		}),
		('Tagging', {
			'fields': ('category', 'tags',)
		}),
		('Banner Image', {
			'fields': ('image', 'caption', 'cropping')
		})
	)

	def _thumbnail(self, obj):
		return thumbnail(obj.image)

	_thumbnail.short_description = u'Banner Image'
	_thumbnail.allow_tags = True

	def author(self, obj):
		return obj.user

	def save_model(self, request, obj, form, change):
		if not change:
			obj.user = request.user
		obj.save()

	def queryset(self, request):
		return Entry.objects.filter(user=request.user)

	class Media:
		js = (settings.STATIC_URL + 'blog/j/admin.js',)

admin.site.register(Entry, EntryAdmin)


class BaseTaggingAdmin(admin.ModelAdmin):
	fields = ['name', 'slug']
	prepopulated_fields = {"slug": ("name",)}
	actions = ['delete_selected_tagging_objects']
	
	def delete_selected_tagging_objects(self, request, queryset):
		pass
	
	def delete_tagging_object(self, entries, instance, request):
		len_entries = len(entries)
		if len_entries == 0:
			instance.delete()
		else:
			single = unicode(instance.__class__._meta.verbose_name)
			plural = unicode(instance.__class__._meta.verbose_name_plural)
			if len_entries == 1:
				entries_prefix = 'this'
				entries_suffix = 'entry'
				cat_prefix = 'its'
				cat_suffix = single
			else:
				entries_prefix = 'these'
				entries_suffix = 'entries'
				cat_prefix = 'their'
				cat_suffix = plural

			messages.error(request, 'The %s %s is unable to be deleted as it is associated with %d %s. Delete %s %s, or change %s %s before trying to delete this %s.' % (instance, single, len_entries, entries_suffix, entries_prefix, entries_suffix, cat_prefix, cat_suffix, single))
			return False
			
		return True
		
	def successful_deletion(self, target, queryset, className, request):
		if len(queryset) == 1:
			message_bit = '%s was' % unicode(className._meta.verbose_name)
		else:
			message_bit = '%s were' % unicode(className._meta.verbose_name_plural)
		
		target.message_user(request, "%d %s successfully deleted." % (len(queryset), message_bit))


class CategoryAdmin(BaseTaggingAdmin):
	def get_actions(self, request):
		return delete_selected_actions(CategoryAdmin, self, request)
	
	def delete_selected_tagging_objects(self, request, queryset):
		for category in queryset:
			if category.can_delete:
				if not super(CategoryAdmin, self).delete_tagging_object(Entry.objects.filter(category=category), category, request):
					return False
			else:
				messages.error(request, 'The %s category is unable to be deleted.' % category)
				return False

		self.successful_deletion(self, queryset, Category, request)
				
	delete_selected_tagging_objects.short_description = 'Delete selected Categories'

admin.site.register(Category, CategoryAdmin)


class TagAdmin(BaseTaggingAdmin):
	def get_actions(self, request):
		return delete_selected_actions(TagAdmin, self, request)
	
	def delete_selected_tagging_objects(self, request, queryset):
		for tag in queryset:
			if not super(TagAdmin, self).delete_tagging_object(Entry.objects.filter(tags=tag), tag, request):
				return False

		self.successful_deletion(self, queryset, Tag, request)
				
	delete_selected_tagging_objects.short_description = 'Delete selected Tags'

admin.site.register(Tag, TagAdmin)