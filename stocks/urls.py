from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('stocks.views',

	url(r'^$', 'index'),
	url(r'^quotes$', 'quotes'),
	url(r'^login', 'login'),
	url(r'^logout', 'logout'),
	url(r'^register', 'register'),
)
