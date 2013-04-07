from django.contrib import admin
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('user', 'title', 'topic')
admin.site.register(Article, ArticleAdmin)

