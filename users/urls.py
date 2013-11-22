from django.conf.urls import patterns, include, url

urlpatterns = patterns('users.views',
	url(r'^register/$', 'register'),
	url(r'^create/$', 'create'),
	url(r'^login/$', 'login'), 
	url(r'^logout/$', 'logout_view'),
	url(r'^profile/$', 'profile'),
	url(r'^add_stock/$', 'addStock'),
	url(r'^remove_stock/$', 'removeStock')
)