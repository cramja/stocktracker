from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'stocktracker.views.index'),
    url(r'^testvisuals/$', 'stocktracker.views.testvisuals'),
    url(r'^admin/', include(admin.site.urls)),
)
