#coding: utf-8

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
import os
import uuid

def article_upload_to(instance, filename):
	user = instance.user
	first_name = user.full_name.split()[0]
	path = 'articles/'
	filename = "%s-%s.pdf" % (slugify(first_name), uuid.uuid4())
	return os.path.join(path, filename)
	
class WictUserManager(BaseUserManager):
	def create_user(self, email, full_name, password=None):
		if not email:
			msg = _('Users must have an email address')
			raise ValueError(msg)

		if not full_name:
			msg = _('Users must have a name')
			raise ValueError(msg)

		user = self.model(
			email=WictUserManager.normalize_email(email),
			full_name=full_name
		)

		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def create_superuser(self, email, full_name, password=None):
		user = self.create_user(email, full_name, password)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class WictUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(
		_('Email address'),
		max_length=254,
		unique=True,
		db_index=True
	)

	full_name = models.CharField(max_length=255)
	is_reviewer = models.BooleanField(default=False)

	# django-admin fields
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	objects = WictUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['full_name']

	def get_full_name(self):
		return self.full_name
	
	def get_short_name(self):
		return self.full_name.split()[0]
	
	def __unicode__(self):
		return self.email

class Author(models.Model):
	article = models.ForeignKey('Article')
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

	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	title = models.CharField(max_length=255, verbose_name='Título')
	abstract = models.TextField(verbose_name='Resumo')
	topic = models.CharField(max_length=2, choices=TOPIC_CHOICES,verbose_name='Assunto principal')
	file = models.FileField(upload_to=article_upload_to, verbose_name='Arquivo')

