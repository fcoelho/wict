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


from wict.forms import WictRegistrationForm
def create_user_profile(sender, user, request, **kwargs):
	form = WictRegistrationForm(request.POST)
	profile = UserProfile(
		user=user,
		full_name=form.data['full_name'],
		is_reviewer=False
	)
	profile.save()

from registration.signals import user_registered
user_registered.connect(create_user_profile)
