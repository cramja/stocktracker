from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('stocks.views',

    url(r'^$', 'index'),
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
    url(r'^register$', 'register'),
    url(r'^create$', 'create'),

    url(r'^get_stocks$', 'getStocks'),
    url(r'^add_stock$', 'addStock'),
    url(r'^remove_stock$', 'removeStock'),

    url(r'^admin/', include(admin.site.urls)),
)
