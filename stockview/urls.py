from django.conf.urls import patterns, include, url

urlpatterns = patterns('stockview.views',
	url(r'^$', 'index'),
)