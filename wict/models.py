#coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)

	full_name = models.CharField(max_length=100)
	is_reviewer = models.BooleanField(default=False)

	def get_absolute_url(self):
		return ('profiles_profile_detail', (), {'username': self.user.username})
	get_absolute_url = models.permalink(get_absolute_url)

class Author(models.Model):
	article = models.ForeignKey('Article')
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	binding = models.CharField(max_length=30)

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

	user = models.ForeignKey(User)
	title = models.CharField(max_length=255)
	abstract = models.TextField()
	topic = models.CharField(max_length=2, choices=TOPIC_CHOICES)

def create_user_profile(sender, user, request, **kwargs):
	from wict.forms import WictRegistrationForm
	form = WictRegistrationForm(request.POST)
	profile = UserProfile(
		user=user,
		full_name=form.data['full_name'],
		is_reviewer=False
	)
	profile.save()

from registration.signals import user_registered
user_registered.connect(create_user_profile)
