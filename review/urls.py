from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(
		r'^$',
		'review.views.reviews',
		name='website_reviews'
	),
	url(
		r'^(?P<review_id>\d+)/$',
		'review.views.display_review',
		name='website_reviews_display'
	)
)
