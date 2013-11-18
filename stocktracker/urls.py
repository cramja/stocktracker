from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'stocktracker.views.index'),
	url(r'^testvisuals/$', 'stocktracker.views.testvisuals'),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^accounts/login/$',  login, ),
	url(r'^accounts/logout/$', logout, {'template_name': 'registration/loggedout.html'}),
	url(r'^accounts/profile/$', 'stocktracker.views.testvisuals'),
	url(r'^accounts/register/$', 'stocktracker.views.register'),
)
