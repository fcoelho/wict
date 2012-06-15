from django import template
register = template.Library()

@register.inclusion_tag('templatetags/wict_form.html')
def wict_form(form):
	return {'form' : form}

@register.inclusion_tag('templatetags/wict_formset.html')
def wict_formset(formset):
	return {'formset' : formset}