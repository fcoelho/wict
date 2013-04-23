# coding: utf-8

from django import forms
from django.utils.safestring import mark_safe

from .models import Review, Criteria

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
					'placeholder': 'Comentários...',
					'rows': '5',
				}
			),
		}

from django.forms.models import inlineformset_factory

ReviewFormSet = inlineformset_factory(Review, Criteria, form=CriteriaForm, can_delete=False, extra=0)
