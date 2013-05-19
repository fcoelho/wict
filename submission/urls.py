from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(
		'^$',
		'submission.views.submission',
		name='website_submission'
	),
	url(
		'^new/$',
		'submission.views.new_submission',
		name='website_submission_new',
	),
	url(
		'^edit/$',
		'submission.views.edit_submission',
		name='website_submission_edit'
	),
	url(
		'^delete/$',
		'submission.views.delete_submission',
		name='website_submission_delete'
	),
	url(
		'^comments/$',
		'submission.views.show_comments',
		name='website_submission_comments'
	)
)

