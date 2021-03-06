# coding: utf-8

from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.forms.models import inlineformset_factory
from .models import Article, Author
import pyPdf

class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		exclude = ('author', 'reviews', 'status')
	
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

