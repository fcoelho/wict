# coding: utf-8

import os
import uuid

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify

def article_upload_to(instance, filename):
	author = instance.author
	first_name = author.full_name.split()[0]
	path = 'articles/'
	filename = "%s-%s.pdf" % (slugify(first_name), uuid.uuid4())
	return os.path.join(path, filename)

class Author(models.Model):
	article = models.ForeignKey('Article', related_name='author_set')
	first_name = models.CharField(max_length=30, verbose_name='Primeiro nome')
	last_name = models.CharField(max_length=30, verbose_name='Último nome')
	binding = models.CharField(max_length=30, verbose_name='Vínculo (instituição)')

class Article(models.Model):
	TOPIC_CHOICES = (
		('BD', 'Banco de dados'),
		('CG', 'Computação gráfica'),
		('PI', 'Processamento de imagens'),
		('IA', 'Inteligência computacional'),
		('MM', 'Sistemas web e multimídia interativos'),
		('AC', 'Arquitetura de computadores'),
		('ES', 'Engenharia de software'),
		('SD', 'Sistemas distribuídos'),
		('PC', 'Programação concorrente'),
		('SE', 'Sistemas embarcados'),
		('RB', 'Robótica'),
		('XX', 'Outro')
	)

	STATUS_CHOICES = (
		('EN', 'Enviado'),
		('ER', 'Em revisão'),
		('AP', 'Aprovado'),
		('RJ', 'Rejeitado')
	)

	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	title = models.CharField(max_length=255, verbose_name='Título')
	abstract = models.TextField(verbose_name='Resumo')
	topic = models.CharField(max_length=2, choices=TOPIC_CHOICES, verbose_name='Assunto principal')
	file = models.FileField(upload_to=article_upload_to, verbose_name='Arquivo')
	reviews = models.ManyToManyField('website.WictUser', through='review.Review', related_name='reviews_set')
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='EN', verbose_name='Estado atual')

	def __unicode__(self):
		return self.title

