#coding: utf-8

from django import forms
from registration.forms import RegistrationForm


class WictRegistrationForm(RegistrationForm):
	full_name = forms.CharField(
		max_length=100,
		help_text='Nome como aparecerá no certificado',
		label='Nome completo'
	)

	def __init__(self, *args, **kwargs):
		RegistrationForm.__init__(self, *args, **kwargs)
		self.fields.keyOrder = [
			'full_name',
			'username',
			'email',
			'password1',
			'password2'
		]

class WictProfileEditForm(forms.ModelForm):
	class Meta:
		from wict.models import UserProfile
		model = UserProfile
		exclude = ('user', 'is_reviewer')
