from django import template
register = template.Library()

@register.inclusion_tag('templatetags/wict_form.html')
def wict_form(form):
	return {'form' : form}

@register.inclusion_tag('templatetags/wict_dynamicformset.html')
def wict_dynamicformset(formset, legend):
	return {'formset' : formset, 'legend' : legend}
	
@register.inclusion_tag('templatetags/wict_formset.html')
def wict_formset(formset, legend):
	return {'formset' : formset, 'legend' : legend}