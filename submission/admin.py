# coding: utf-8

from collections import OrderedDict
from functools import update_wrapper

from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

from signup.utils import send_email

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
		reviews = filter(lambda x: x.reviewed(), Review.objects.filter(article=article))

		if request.method == 'POST':
			if 'approve' in request.POST:
				messages.success(request, _(u'Artigo aprovado'))
				approved = True
			elif 'reject' in request.POST:
				messages.success(request, _(u'Artigo rejeitado'))
				approved = False
			else:
				approved = None
				messages.warning(request, _(u'Ação inválida, tente novamente'))

			if approved is not None:
				article.status = 'AP' if approved else 'RJ'
				article.save()

				self.send_review_email(article, approved)

				return redirect('admin:submission_article_changelist')

		if not reviews:
			messages.warning(request, _(u'Este artigo ainda não tem revisões o suficiente para ser avaliado'))
			return redirect('admin:submission_article_changelist')

		data_by_criterias = OrderedDict()
		for review in reviews:
			criterias = review.criteria_set.all()
			for crit in criterias:
				if crit.attribute not in data_by_criterias:
					data_by_criterias[crit.attribute] = [[], []]
				data_by_criterias[crit.attribute][0].append(crit.value)
				data_by_criterias[crit.attribute][1].append(crit.comment)
			ev = review.evaluation
			if ev.attribute not in data_by_criterias:
				data_by_criterias[ev.attribute] = [[], []]
			data_by_criterias[ev.attribute][0].append(ev.value)
			data_by_criterias[ev.attribute][1].append(ev.comment)

		opts = Article._meta

		context = {
			'title': _(u'Avaliação de artigo'),
			'module_name': capfirst(force_text(opts.verbose_name_plural)),
			'app_label': opts.app_label,
			'article': article,
			'reviews': reviews,
			'data_by_criterias': data_by_criterias,
		}

		return TemplateResponse(
			request,
			'admin/submission/article_review.html',
			context,
		)

	def send_review_email(self, article, approved):
		type_str = 'approved' if approved else 'rejected'
		template_name = 'admin/submission/%s_email.txt' % type_str

		context = {
			'title': article.title
		}

		to = article.author.email

		send_email(template_name, context, to)

	def author_name(self, article):
		return article.author.full_name
	author_name.short_description = ugettext_lazy(u'Nome do autor')

	def completed(self, article):
		reviews = Review.objects.filter(article=article)
		evaluated = filter(lambda x: x.reviewed(), reviews)
		return u'%i/%i' % (len(evaluated), len(reviews))
	completed.short_description = ugettext_lazy(u'Revisões completadas')

	def review(self, article):
		url = reverse('admin:article_admin_review', args=(article.pk,))
		return _('<a href="%s">Avaliar</a>') % url
	review.allow_tags = True
	review.short_description = ugettext_lazy('Avaliar')

	list_display = ('author_name', 'title', 'topic', 'status', 'completed', 'review')

admin.site.register(Article, ArticleAdmin)

