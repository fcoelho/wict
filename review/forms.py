# coding: utf-8

from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from .models import Review, Criteria, Evaluation

class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review

class CriteriaForm(forms.ModelForm):
	class Meta:
		model = Criteria
		widgets = {
			'review': forms.HiddenInput,
			'attribute': forms.HiddenInput,
			'help_text': forms.HiddenInput,
			'value': forms.RadioSelect,
			'comment': forms.Textarea(
				attrs={
					'placeholder': _(u'Comentários...'),
					'rows': '5',
				}
			),
		}

class EvaluationForm(CriteriaForm):
	class Meta(CriteriaForm.Meta):
		model = Evaluation

ReviewFormSet = inlineformset_factory(Review, Criteria, form=CriteriaForm, can_delete=False, extra=0)
