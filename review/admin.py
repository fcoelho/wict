from django import forms

from django.contrib import admin

from submission.models import Article
from .models import Review

class ReviewForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ReviewForm, self).__init__(*args, **kwargs)
		#self.fields['article'].queryset = Article.review_set.exclude(

	class Meta:
		model = Review

class ReviewAdmin(admin.ModelAdmin):
	def reviewer_name(self, review):
		return review.reviewer.get_full_name()
	def article_title(self, review):
		return review.article.title

	list_display = ('reviewer_name', 'article_title')
	form = ReviewForm
admin.site.register(Review, ReviewAdmin)

