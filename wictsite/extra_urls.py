#coding: utf-8

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from registration.views import activate
from registration.views import register

from wict.forms import WictRegistrationForm, WictProfileEditForm

from django.contrib.auth import views as auth_views

from wict import views as wict_views
from profiles import views

#Views de registro
urlpatterns = patterns('',
	url(r'^activate/complete/$',
		direct_to_template,
		{'template': 'registration/activation_complete.html'},
		name='registration_activation_complete'),
	# Activation keys get matched by \w+ instead of the more specific
	# [a-fA-F0-9]{40} because a bad activation key should still get to the view;
	# that way it can return a sensible "invalid key" message instead of a
	# confusing 404.
	url(r'^activate/(?P<activation_key>\w+)/$',
		activate,
		{'backend': 'registration.backends.default.DefaultBackend'},
		name='registration_activate'),
	url(r'^register/$',
		register,
		{
			'backend': 'registration.backends.default.DefaultBackend',
			'form_class': WictRegistrationForm
		},
		name='registration_register'),
	url(r'^register/complete/$',
		direct_to_template,
		{'template': 'registration/registration_complete.html'},
		name='registration_complete'),
	url(r'^register/closed/$',
		direct_to_template,
		{'template': 'registration/registration_closed.html'},
		name='registration_disallowed'),
)

#Views de autenticação padrão do Django
urlpatterns += patterns('',
	url(r'^login/$',
		wict_views.wict_login,
		{'template_name': 'registration/login.html'},
		name='auth_login'),
	url(r'^logout/$',
		auth_views.logout,
		{'template_name': 'registration/logout.html'},
		name='auth_logout'),
	url(r'^password/change/$',
		auth_views.password_change,
		{'template_name': 'registration/password_change.html'},
		name='auth_password_change'),
	url(r'^password/change/done/$',
		auth_views.password_change_done,
		{'template_name': 'registration/password_change_complete.html'},
		name='auth_password_change_done'),
	url(r'^password/reset/$',
		auth_views.password_reset,
		{'template_name': 'registration/password_reset.html'},
		name='auth_password_reset'),
	url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
		auth_views.password_reset_confirm,
		{'template_name': 'registration/password_reset_confirmation.html'},
		name='auth_password_reset_confirm'),
	url(r'^password/reset/complete/$',
		auth_views.password_reset_complete,
		{'template_name': 'registration/password_reset_form_complete.html'},
		name='auth_password_reset_complete'),
	url(r'^password/reset/done/$',
		auth_views.password_reset_done,
		{'template_name': 'registration/password_reset_form_done.html'},
		name='auth_password_reset_done'),
)

#Views de profiles
urlpatterns += patterns('',
	url(r'^create/$',
		views.create_profile,
		name='profiles_create_profile'),
	url(r'^edit/$',
		views.edit_profile,
		{'form_class': WictProfileEditForm},
		name='profiles_edit_profile'),
	url(r'^(?P<username>\w+)/$',
		views.profile_detail,
		name='profiles_profile_detail'),
	url(r'^$',
		views.profile_list,
		name='profiles_profile_list'),
)
