# coding: utf-8

import logging

from django.db import models
from django.conf import settings

from submission.models import Article

logger = logging.getLogger(__name__)


class Review(models.Model):
	reviewer = models.ForeignKey(
		'website.WictUser',
		limit_choices_to={'is_reviewer': True}
	)
	article = models.ForeignKey('submission.Article')
	comment = models.TextField()

	class Meta:
		unique_together = ('reviewer', 'article')

	def save(self, *args, **kwargs):
		created = not self.pk

		super(Review, self).save(*args, **kwargs)

		# if the model was just created, add the new criteria instances
		if created:
			attrs = [
				'Originalidade',
				'Qualidade',
				'Relevância',
				'Apresentação'
			]

			for attr in attrs:
				c = Criteria(review=self, attribute=attr)
				c.save()


class Criteria(models.Model):
	VALUES = (
		(1, 'weak'),
		(2, 'below average'),
		(3, 'average'),
		(4, 'good'),
		(5, 'excellent')
	)

	review = models.ForeignKey(Review)

	attribute = models.CharField(max_length=64)
	value = models.IntegerField(default=1, choices=VALUES)
