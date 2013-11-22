from django.conf.urls import patterns, include, url

urlpatterns = patterns('users.views',
	url(r'^register/$', 'register'),
	url(r'^create/$', 'create'),
	url(r'^login/$', 'login'), #new login using django.admin function
	url(r'^logout/$', 'logout_view'),
	url(r'^profile/$', 'profile'),
	url(r'^add_stock/$', 'addStock')
)