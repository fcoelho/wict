# coding: utf-8

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

class WictUserManager(BaseUserManager):
	def create_user(self, email, full_name, password=None):
		if not email:
			msg = _(u'Usuários devem ter um endereço de e-email')
			raise ValueError(msg)

		if not full_name:
			msg = _(u'Usuários devem ter um nome')
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
		_(u'Endereço de e-mail'),
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

