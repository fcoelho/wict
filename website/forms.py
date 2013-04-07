#coding: utf-8

from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from .models import Article, Author, WictUser
import pyPdf

class UserSignUpForm(forms.Form):
	email = forms.EmailField(label=_('E-mail'))
	full_name = forms.CharField(label=_('Full name'), max_length=255)
	password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
	password2 = forms.CharField(label=_('Confirm password'), widget=forms.PasswordInput)

	def clean_email(self):
		email = self.cleaned_data['email'].strip()
		try:
			WictUser.objects.get(email__iexact=email)
			raise forms.ValidationError(_('An user with that e-mail already exists'))
		except WictUser.DoesNotExist:
			return email

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(_("The two passwords didn't match"))
		return password2

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
				try:
					f = pyPdf.PdfFileReader(file)
				except:
					raise forms.ValidationError("Não é um arquivo PDF válido")
				if f.getNumPages() > settings.MAX_ARTICLE_PAGES:
					raise forms.ValidationError(
						"O artigo deve ter no máximo %i páginas" %
						settings.MAX_ARTICLE_PAGES
					)
				return file
		else:
			raise ValidationError("Este campo é obrigatório")

class AuthorForm(forms.ModelForm):
	class Meta:
		model = Author
		exclude = ('article',)

AuthorFormSet = inlineformset_factory(Article, Author, can_delete=False, extra=1)

