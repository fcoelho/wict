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
