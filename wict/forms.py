#coding: utf-8

from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.forms.models import inlineformset_factory
from registration.forms import RegistrationForm
from wict.models import UserProfile, Article, Author

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
		model = UserProfile
		exclude = ('user', 'is_reviewer')

class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		exclude = ('user',)
	
	def clean_file(self):
		file = self.cleaned_data.get('file', False)
		if file:
			if file.size > settings.MAX_ARTICLE_FILE_SIZE:
				raise forms.ValidationError(u"Arquivo é maior que %s"
					% filesizeformat(settings.MAX_ARTICLE_FILE_SIZE))
			else:
				return file
		else:
			raise ValidationError("Meu erro custom")

class AuthorForm(forms.ModelForm):
	class Meta:
		model = Author
		exclude = ('article',)

AuthorFormSet = inlineformset_factory(Article, Author, can_delete=False, extra=1)








