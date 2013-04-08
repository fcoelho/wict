from django.db import models
from django.conf import settings

from submission.models import Article

class Review(models.Model):
	reviewer = models.ForeignKey(
		'website.WictUser',
		limit_choices_to = {'is_reviewer': True}
	)
	article = models.ForeignKey('submission.Article')

	class Meta:
		unique_together = ('reviewer', 'article')

