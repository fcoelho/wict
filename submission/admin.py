# coding: utf-8

from functools import update_wrapper

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

from review.models import Review
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
	def get_urls(self):
		from django.conf.urls import patterns, url

		def wrap(view):
			def wrapper(*args, **kwargs):
				return self.admin_site.admin_view(view)(*args, **kwargs)
			return update_wrapper(wrapper, view)

		urls = super(ArticleAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^(.+)/review/$',
				wrap(self.review_view),
				name='article_admin_review'
			)
		)

		# my_urls must come before the default urls because urls has a
		# catch-all r'^(.+)/$' pattern
		return my_urls + urls

	def review_view(self, request, object_id):
		article = get_object_or_404(Article, pk=object_id)
		reviews = Review.objects.filter(article=article)

		opts = Article._meta

		context = {
			'title': _(u'Avaliação de artigo'),
			'module_name': capfirst(force_text(opts.verbose_name_plural)),
			'app_label': opts.app_label,
			'article': article,
			'reviews': reviews,
		}

		return TemplateResponse(
			request,
			'admin/submission/article_review.html',
			context,
		)

	def review(self, article):
		url = reverse('admin:article_admin_review', args=(article.pk,))
		return _('<a href="%s">Avaliar</a>') % url
	review.allow_tags = True
	review.short_description = ugettext_lazy('Avaliar')

	list_display = ('author', 'title', 'topic', 'status', 'review')

admin.site.register(Article, ArticleAdmin)

