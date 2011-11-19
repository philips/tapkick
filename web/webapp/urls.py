from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^users/(?P<rfid_id>\w+)/$', 'beer.views.user_detail', name='user_detail'),
    url(r'^users/$', 'beer.views.user_list', name='user_list'),
    url(r'^$', 'beer.views.front_page', name='front_page'),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
