from django.contrib import admin
from wict.models import UserProfile, Article

class UserProfileAdmin(admin.ModelAdmin):
	pass
admin.site.register(UserProfile, UserProfileAdmin)

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('user', 'title', 'topic')
admin.site.register(Article, ArticleAdmin)
