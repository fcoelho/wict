from django.contrib import admin
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
	def review(self, article):
		return unicode('<a href="http://www.google.com">Avaliar</a>')
	review.allow_tags = True
	review.short_description = 'Avaliar'

	list_display = ('author', 'title', 'topic', 'status', 'review')

admin.site.register(Article, ArticleAdmin)

