from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('stocks.views',
	url(r'^stockview/', include('stockview.urls')),
	url(r'^users/', include('users.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^stocks/$', 'stocks'),
)
