# coding: utf-8

from django import forms

from django.contrib import admin
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _

from submission.models import Article
from .models import Review, Criteria, Evaluation

class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review

class ReviewAdmin(admin.ModelAdmin):
	def reviewer_name(self, review):
		return review.reviewer.get_full_name()
	reviewer_name.short_description = _(u'Nome do revisor')

	def article_title(self, review):
		return review.article.title
	article_title.short_description = _(u'Título do artigo')

	def article_count(self, review):
		return unicode(Review.objects.filter(reviewer=review.reviewer).count())
	article_count.short_description = _(u'Quantidade de artigos para o revisor')

	list_display = ('reviewer_name', 'article_count', 'article_title')
	form = ReviewForm

class CriteriaAdmin(admin.ModelAdmin):
	def short_comment(self, criteria):
		return truncatechars(criteria.comment, 64)
	short_comment.short_description = _(u'Comentário')

	list_display = ('review', 'attribute', 'value', 'short_comment')

class EvaluationAdmin(admin.ModelAdmin):
	def short_comment(self, evaluation):
		return truncatechars(evaluation.comment, 64)
	short_comment.short_description = _(u'Comentário')

	list_display = ('review', 'attribute', 'value', 'short_comment')

admin.site.register(Review, ReviewAdmin)
admin.site.register(Criteria, CriteriaAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
