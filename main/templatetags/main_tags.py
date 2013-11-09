from django import template

from main.models import Servicio

register = template.Library()

@register.simple_tag
def active(request, pattern):
	import re
	if re.search(pattern, request.path):
		return 'active'
	return ''

@register.filter
def labelizar(estado):
	if estado == Servicio.EN_COLA:
		return 'label-danger'
	elif estado == Servicio.EN_REVISION:
		return 'label-warning'
	elif estado == Servicio.REPARADO:
		return 'label-success'
	else:
		return 'label-info'