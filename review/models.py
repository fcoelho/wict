# coding: utf-8

import logging

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy
from django.utils.translation import ugettext as _

from submission.models import Article

logger = logging.getLogger(__name__)


class Review(models.Model):
	reviewer = models.ForeignKey(
		'website.WictUser',
		limit_choices_to={'is_reviewer': True},
		verbose_name=ugettext_lazy(u'Revisor')
	)
	article = models.ForeignKey('submission.Article', verbose_name=ugettext_lazy(u'Artigo'))

	class Meta:
		unique_together = ('reviewer', 'article')
		verbose_name = ugettext_lazy(u'revisão')
		verbose_name_plural = ugettext_lazy(u'revisões')

	def save(self, *args, **kwargs):
		created = not self.pk

		super(Review, self).save(*args, **kwargs)

		# if the model was just created, add the new criteria instances
		if created:
			attrs = [
				(_(u'Originalidade'), u''),
				(_(u'Qualidade'), _(u'Qualidade técnica, metodológica, analítica')),
				(_(u'Relevância'), u''),
				(_(u'Apresentação'), _(u'Legibilidade, clareza da apresentação, organização das ideias')),
				(_(u'Confiança do revisor'), _(u'Quão confiante você está sobre a avaliação deste artigo?')),
			]

			for attr in attrs:
				c = Criteria(review=self, attribute=attr[0], help_text=attr[1])
				c.save()

			e = Evaluation(
				review=self,
				attribute=_(u'Avaliação'),
				help_text=_(
					u'Dê seu parecer sobre o artigo, e se deve ser aprovado.\n'
					u'Se quiser mandar mensagens específicas para a banca,'
					u'deixe indicado'
				)
			)
			e.save()

			# update the status. the author will see the article is now being
			# reviewed
			self.article.status = 'ER'
			self.article.save()
		else:
			# since we're saving a previously created review, we have to
			# set the article status accordingly
			pass
	
	def reviewed(self):
		return self.evaluation.value > 0

	def __unicode__(self):
		return self.reviewer.full_name + u':' + self.article.author.full_name

class CriteriaBase(models.Model):
	class Meta:
		abstract = True

	attribute = models.CharField(ugettext_lazy(u'Atributo'), max_length=64)
	comment = models.TextField(ugettext_lazy(u'Comentário'), blank=True)
	help_text = models.CharField(ugettext_lazy(u'Texto de ajuda'), max_length=255, blank=True)

class Criteria(CriteriaBase):
	VALUES = (
		(1, ugettext_lazy(u'Fraco')),
		(2, ugettext_lazy(u'Abaixo da média')),
		(3, ugettext_lazy(u'Médio')),
		(4, ugettext_lazy(u'Bom')),
		(5, ugettext_lazy(u'Excelente'))
	)

	review = models.ForeignKey(Review, verbose_name=ugettext_lazy(u'Revisão'))
	value = models.IntegerField(ugettext_lazy(u'Valor'), default=-1, choices=VALUES)

	class Meta:
		verbose_name = ugettext_lazy(u'critério de avaliação')
		verbose_name_plural = ugettext_lazy(u'critérios de avaliação')

class Evaluation(CriteriaBase):
	VALUES = (
		(1, ugettext_lazy(u'Rejeitado')),
		(2, ugettext_lazy(u'Rejeitado fraco')),
		(3, ugettext_lazy(u'Neutro')),
		(4, ugettext_lazy(u'Aprovado fraco')),
		(5, ugettext_lazy(u'Aprovado'))
	)

	review = models.OneToOneField(Review, verbose_name=ugettext_lazy(u'Revisão'))
	value = models.IntegerField(ugettext_lazy(u'Valor'), default=-1, choices=VALUES)

	class Meta:
		verbose_name = ugettext_lazy(u'avaliação final')
		verbose_name_plural = ugettext_lazy(u'avaliações finais')
