from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'stocktracker.views.index'),
    url(r'^visuals/$', 'stocktracker.views.visuals'),
    url(r'^admin/', include(admin.site.urls)),
)
