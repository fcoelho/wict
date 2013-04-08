from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(
		r'^$',
		'review.views.reviews',
		name='website_reviews'
	),
)
