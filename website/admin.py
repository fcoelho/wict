from django.core.urlresolvers import reverse
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from signup.utils import send_email

from .models import WictUser

class WictUserAdmin(admin.ModelAdmin):
	def send_review_email(self, request, queryset):
		reviewers = queryset.filter(is_reviewer=True)
		for reviewer in reviewers:
			full_url = request.build_absolute_uri(reverse('website_reviews'))
			context = {
				"full_url": full_url
			}

			# this template is loaded from a different app... but it makes
			# so much more sense to place that template there
			send_email(
				'admin/review/articles_to_review_email.txt',
				context,
				reviewer.email
			)

		msg = u'Foram enviados emails para os seguintes revisores: (%i)'
		self.message_user(request, _(msg % len(reviewers)))
		for reviewer in reviewers:
			self.message_user(request, reviewer.get_full_name())


	def submitted_article(self, user):
		return user.article_set.count() != 0
	submitted_article.boolean = True
	submitted_article.short_description = _(u'Submeteu artigo')

	list_display = ('full_name', 'email', 'submitted_article', 'is_reviewer', 'is_active')
	list_filter = ('is_reviewer', 'is_admin', 'is_staff', 'is_active')
	actions = ['send_review_email']

admin.site.register(WictUser, WictUserAdmin)

