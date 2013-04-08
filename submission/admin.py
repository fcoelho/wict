from django.contrib import admin
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('author', 'title', 'topic')
admin.site.register(Article, ArticleAdmin)

