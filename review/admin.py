from django import forms

from django.contrib import admin

from submission.models import Article
from .models import Review, Criteria

class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review

class ReviewAdmin(admin.ModelAdmin):
	def reviewer_name(self, review):
		return review.reviewer.get_full_name()
	def article_title(self, review):
		return review.article.title
	def article_count(self, review):
		return unicode(Review.objects.filter(reviewer=review.reviewer).count())

	list_display = ('reviewer_name', 'article_count', 'article_title')
	form = ReviewForm

admin.site.register(Review, ReviewAdmin)
admin.site.register(Criteria)
