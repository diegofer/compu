# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm #, UserCreationForm
from django.conf import settings

from main.models import Servicio


def home(request, estado='todos'):
	todos = Servicio.objects.all()
	if estado == 'todos':
		servicios = todos
	else:
		servicios = Servicio.objects.filter(estado__exact=estado)

	num_cola = todos.filter(estado__exact=Servicio.EN_COLA).count()
	num_revision = todos.filter(estado__exact=Servicio.EN_REVISION).count()
	num_reparado = todos.filter(estado__exact=Servicio.REPARADO).count()
	num_entregado = todos.filter(estado__exact=Servicio.ENTREGADO).count()

	estados = Servicio.ESTADO

	ctx = {'servicios': servicios, 'estados':Servicio.ESTADO}  # estado es el model0 vacio para tener en la plantilla las variables estaticas..
	return render_to_response('main/home.html', locals(), context_instance=RequestContext(request))

