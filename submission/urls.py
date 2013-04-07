from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(
		'^submission/$',
		'submission.views.submission',
		name='website_submission'
	),
	url(
		'^submission/new/$',
		'submission.views.new_submission',
		name='website_submission_new',
	),
	url(
		'^submission/edit/$',
		'submission.views.edit_submission',
		name='website_submission_edit'
	),
	url(
		'^submission/delete/$',
		'submission.views.delete_submission',
		name='website_submission_delete'
	)
)

