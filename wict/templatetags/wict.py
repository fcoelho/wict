from django import template
register = template.Library()

@register.inclusion_tag('templatetags/wict_form.html')
def wict_form(form):
	return {'form' : form}
