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

	class Meta:
		unique_together = ('reviewer', 'article')

	def save(self, *args, **kwargs):
		created = not self.pk

		super(Review, self).save(*args, **kwargs)

		# if the model was just created, add the new criteria instances
		if created:
			attrs = [
				('Originalidade', ''),
				('Qualidade', 'Qualidade técnica, metodológica, analítica'),
				('Relevância', ''),
				('Apresentação', 'Legibilidade, clareza da apresentação, organização das ideias'),
			]

			for attr in attrs:
				c = Criteria(review=self, attribute=attr[0], help_text=attr[1])
				c.save()


class Criteria(models.Model):
	VALUES = (
		(1, 'Fraco'),
		(2, 'Abaixo da média'),
		(3, 'Médio'),
		(4, 'Bom'),
		(5, 'Excelente')
	)

	review = models.ForeignKey(Review)

	attribute = models.CharField(max_length=64)
	value = models.IntegerField(default=1, choices=VALUES)
	comment = models.TextField()
	help_text = models.CharField(max_length=255, blank=True)
