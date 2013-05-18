# coding: utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import WictUser

class UserSignUpForm(forms.Form):
	email = forms.EmailField(label=_('E-mail'))
	full_name = forms.CharField(label=_('Nome completo'), max_length=255)
	password1 = forms.CharField(label=_('Senha'), widget=forms.PasswordInput)
	password2 = forms.CharField(label=_('Repetir senha'), widget=forms.PasswordInput)

	def clean_email(self):
		email = self.cleaned_data['email'].strip()
		try:
			WictUser.objects.get(email__iexact=email)
			raise forms.ValidationError(_(u'Um usuário com este e-mail já existe'))
		except WictUser.DoesNotExist:
			return email

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(_("As senhas não correspondem, insira-as novamente"))
		return password2

