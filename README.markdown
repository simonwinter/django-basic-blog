# Requirements

This Django application requires the following:

* Django 1.3.1 and above: it was built against 1.3.1, but may work with other versions of 1.3.
* sorl thumbnail [http://thumbnail.sorl.net](http://thumbnail.sorl.net)
* django tiny mce [http://code.google.com/p/django-tinymce/](http://code.google.com/p/django-tinymce/)


## Settings

The following settings are required to activate this app as intended.

### settings.py

    TINYMCE_JS_URL = '/media/tiny_mce/tiny_mce.js'
    TINYMCE_DEFAULT_CONFIG = {
	    'theme' : "advanced", 
	    'theme_advanced_toolbar_location' : "top",
        'theme_advanced_toolbar_align' : "left",
        'relative_urls': False,
	'theme_advanced_buttons1' : "bold,italic,separator,link,unlink",
	'theme_advanced_buttons2' : "",
	'theme_advanced_buttons3' : ""
}`

`INSTALLED_APPS = (
    ...
    'blog',
    ...
)`

### urls.py

`urlpatterns = patterns('',
	...
    url(r'^blog/', include('blog.urls')),
    ...
)`

### Media URLs

To use tiny mce in the admin, create a symbolic link to the media/tiny_mce directory located in the python site package for tinymce (or just copy the media/tiny_mce directory to the site's media directory). Once this is done, make sure the setting for `TINYMCE_JS_URL` is correct.

In the media directory, add a symbolic link to `blog/media` - name this link `blog_media`.
