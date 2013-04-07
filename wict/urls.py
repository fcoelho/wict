from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', include('website.urls')),
	url(r'^submission/', include('submission.urls')),
	#url('^review/', include('review.urls')),
	url(r'^accounts/', include('signup.urls')),
	url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




#	url(r'^$', 'wict.views.index'),
#	url(r'^articles/$', 'wict.views.articles'),
#	url(r'^registration/$', 'wict.views.registration'),
#	url(r'^review/$', 'wict.views.review'),
#	url(r'^submission/$',
#		'wict.views.submission',
#		name='submission'),
#	url(r'^submission/new/$',
#		'wict.views.new_submission',
#		name='submission_new'),
#	url(r'^submission/edit/$',
#		'wict.views.edit_submission',
#		name='submission_edit'),
#	url(r'^submission/delete/$',
#		'wict.views.delete_submission',
#		name='submission_delete'),
#    url(r'^admin/', include(admin.site.urls)),
#	url(r'^accounts/', include('wictsite.extra_urls')),
#)

#Pra servir os arquivos em MEDIA_ROOT no servidor de desenvolvimento...
#urlpatterns += patterns('',
#	url(r'^media/(.*)$',
#		'django.views.static.serve',
#		{'document_root' : settings.MEDIA_ROOT}),
#)
