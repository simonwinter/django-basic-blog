from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'blog.views.home'),
    (r'^entry/(?P<slug>[a-z0-9-]+)/$', 'blog.views.entry'),
)