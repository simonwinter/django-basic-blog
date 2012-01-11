from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'blog.views.home'),
    (r'^entry/(?P<slug>[a-z0-9-]+)/$', 'blog.views.entry'),
    (r'^(?P<mode>category|tag)/(?P<slug>[a-z0-9-]+)/$', 'blog.views.category_tag_entries'),
    (r'^user/(?P<user>[a-z0-9-]+)/$', 'blog.views.user'),
)