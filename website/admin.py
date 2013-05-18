from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import WictUser

class WictUserAdmin(admin.ModelAdmin):
	def submitted_article(self, user):
		return user.article_set.count() != 0
	submitted_article.boolean = True
	submitted_article.short_description = _(u'Submeteu artigo')

	list_display = ('full_name', 'email', 'submitted_article', 'is_reviewer', 'is_active')
admin.site.register(WictUser, WictUserAdmin)

