from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wictsite.views.home', name='home'),
    # url(r'^wictsite/', include('wictsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url(r'^$', 'wict.views.index'),
	url(r'^articles/$', 'wict.views.articles'),
	url(r'^registration/$', 'wict.views.registration'),
	url(r'^review/$', 'wict.views.review'),
	url(r'^submission/$', 'wict.views.submission'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/', include('wictsite.auth_urls')),
)
