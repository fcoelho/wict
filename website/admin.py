from django.contrib import admin
from .models import WictUser

class WictUserAdmin(admin.ModelAdmin):
	def submitted_article(self, user):
		return user.article_set.count() != 0
	submitted_article.boolean = True

	list_display = ('full_name', 'email', 'submitted_article', 'is_reviewer', 'is_active')
admin.site.register(WictUser, WictUserAdmin)

