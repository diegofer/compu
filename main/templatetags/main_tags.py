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

@register.filter
def estado_btn(estado, btn_id):
	if estado == Servicio.EN_COLA and btn_id == Servicio.EN_COLA:
		return 'btn-danger active'
	if estado == Servicio.EN_REVISION and btn_id == Servicio.EN_REVISION:
		return 'btn-warning active'
	if estado == Servicio.REPARADO and btn_id == Servicio.REPARADO:
		return 'btn-success active'
	if estado == Servicio.ENTREGADO and btn_id == Servicio.ENTREGADO:
		return 'btn-info active'
	return 'btn-default'