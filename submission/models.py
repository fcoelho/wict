# coding: utf-8

import os
import uuid

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

def article_upload_to(instance, filename):
	author = instance.author
	first_name = author.full_name.split()[0]
	path = 'articles/'
	filename = "%s-%s.pdf" % (slugify(first_name), uuid.uuid4())
	return os.path.join(path, filename)

class Author(models.Model):
	article = models.ForeignKey('Article', related_name='author_set', verbose_name=_(u'Artigo'))
	first_name = models.CharField(max_length=30, verbose_name=_(u'Primeiro nome'))
	last_name = models.CharField(max_length=30, verbose_name=_(u'Último nome'))
	binding = models.CharField(max_length=30, verbose_name=_(u'Vínculo (instituição)'))

	class Meta:
		verbose_name = _(u'autor')
		verbose_name_plural = _(u'autores')

class Article(models.Model):
	TOPIC_CHOICES = (
		('BD', _(u'Banco de dados')),
		('CG', _(u'Computação gráfica')),
		('PI', _(u'Processamento de imagens')),
		('IA', _(u'Inteligência computacional')),
		('MM', _(u'Sistemas web e multimídia interativos')),
		('AC', _(u'Arquitetura de computadores')),
		('ES', _(u'Engenharia de software')),
		('SD', _(u'Sistemas distribuídos')),
		('PC', _(u'Programação concorrente')),
		('SE', _(u'Sistemas embarcados')),
		('RB', _(u'Robótica')),
		('XX', _(u'Outro'))
	)

	STATUS_CHOICES = (
		('EN', _(u'Enviado')),
		('ER', _(u'Em revisão')),
		('AP', _(u'Aprovado')),
		('RJ', _(u'Rejeitado'))
	)

	author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u'Autor'))
	title = models.CharField(max_length=255, verbose_name=_(u'Título'))
	abstract = models.TextField(verbose_name=_(u'Resumo'))
	topic = models.CharField(max_length=2, choices=TOPIC_CHOICES, verbose_name=_(u'Assunto principal'))
	file = models.FileField(upload_to=article_upload_to, verbose_name=_(u'Arquivo'))
	reviews = models.ManyToManyField('website.WictUser', through='review.Review', related_name='reviews_set', verbose_name=_(u'Revisões'))
	status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='EN', verbose_name=_(u'Estado atual'))

	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name = _('artigo')
		verbose_name_plural = _('artigos')

