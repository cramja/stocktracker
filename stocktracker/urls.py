from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^accounts/login/$',  login ),
	url(r'^accounts/logout/$', logout, {'template_name': 'registration/loggedout.html'}),
	url(r'^accounts/profile/$', 'stocktracker.views.profile'),
	url(r'^accounts/register/$', 'stocktracker.views.register'),
	url(r'^accounts/success/$', 'stocktracker.views.success'),

	url(r'^$', 'stocktracker.views.index'), #index page
	url(r'^visuals/$', 'stocktracker.views.visuals'),
	url(r'^admin/', include(admin.site.urls)),
)
