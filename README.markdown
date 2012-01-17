# Requirements

This Django application requires the following:

* Django 1.3.1 and above: it was built against 1.3.1, but may work with other versions of 1.3.
* Django image cropping: https://github.com/jonasundderwolf/django-image-cropping
* easy-thumbnails is recommended, but you should be ok without it https://github.com/SmileyChris/easy-thumbnails
* django tiny mce http://code.google.com/p/django-tinymce/
* `django.contrib.staticfiles` https://docs.djangoproject.com/en/dev/howto/static-files/
* Endless pagination http://code.google.com/p/django-endless-pagination/


## Settings

The following settings are required to activate this app as intended.

### settings.py

	TINYMCE_JS_URL = '/static/blog/j/tiny_mce/tiny_mce.js'
	TINYMCE_DEFAULT_CONFIG = {
		'theme' : "advanced", 
		'theme_advanced_toolbar_location' : "top",
		'theme_advanced_toolbar_align' : "left",
		'relative_urls': False,
		'theme_advanced_buttons1' : "bold,italic,separator,link,unlink",
		'theme_advanced_buttons2' : "",
		'theme_advanced_buttons3' : "",
		'plugins': "paste",
		'paste_auto_cleanup_on_paste' : True,
		'paste_remove_styles' : True,
		'paste_remove_styles_if_webkit' : True,
	    'paste_strip_class_attributes': True,
	}

    INSTALLED_APPS = (
        ...
        'blog',
        ...
    )
    
    # Pagination settings for blog entry views.
	ENDLESS_PAGINATION_PER_PAGE = 3 # change this to whatever suits your page views.
	ENDLESS_PAGINATION_PREVIOUS_LABEL = '&larr;'
	ENDLESS_PAGINATION_NEXT_LABEL = '&rarr;'
    
    # for use with the thumbnail cropping in the admin.
    IMAGE_CROPPING_THUMB_SIZE = (400, 400)
	IMAGE_CROPPING_SIZE = '960x280'

### urls.py

    urlpatterns = patterns('',
	    ...
        url(r'^blog/', include('blog.urls')),
        ...
    )
    
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
