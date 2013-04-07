from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(
		'^$',
		'website.views.index',
		name='website_index'
	),
	url(
		'^articles/$',
		'website.views.articles',
		name='website_articles'
	),
	url(
		'^registration/$',
		'website.views.registration',
		name='website_registration'
	),
	#url('', include('submission.urls')),
	#url('', include('review.urls')),
)
