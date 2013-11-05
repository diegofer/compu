# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm #, UserCreationForm
from django.conf import settings

from main.models import Servicio, Persona
from main.forms import ServicioForm, PersonaForm


def home(request, estado='reciente'):
	if estado == 'reciente':
		servicios = Servicio.objects.all().order_by('-updated')[:20]
	else:
		servicios = Servicio.objects.filter(estado__exact=estado)

	num_cola      = Servicio.objects.filter(estado__exact=Servicio.EN_COLA).count()
	num_revision  = Servicio.objects.filter(estado__exact=Servicio.EN_REVISION).count()
	num_reparado  = Servicio.objects.filter(estado__exact=Servicio.REPARADO).count()
	num_entregado = Servicio.objects.filter(estado__exact=Servicio.ENTREGADO).count()

	SERVICIO = Servicio # estado es el model0 vacio para tener en la plantilla las variables estaticas..
	estado   = estado

	servicioForm = ServicioForm()
	personaForm = PersonaForm()

	
	return render_to_response('main/home.html', locals(), context_instance=RequestContext(request))




def servicio(request, id):
	servicio = Servicio.objects.get(id=id)

	num_cola = Servicio.objects.filter(estado__exact=Servicio.EN_COLA).count()
	num_revision = Servicio.objects.filter(estado__exact=Servicio.EN_REVISION).count()
	num_reparado = Servicio.objects.filter(estado__exact=Servicio.REPARADO).count()
	num_entregado = Servicio.objects.filter(estado__exact=Servicio.ENTREGADO).count()

	SERVICIO = Servicio # estado es el model0 vacio para tener en la plantilla las variables estaticas..
	servicioForm = ServicioForm()
	personaForm = PersonaForm()

	return render_to_response('main/servicio.html', locals(), context_instance=RequestContext(request))




def persona(request, id):
	persona = Persona.objects.get(id=id)
	servicios = Servicio.objects.filter(cliente__pk=persona.id)
	return render_to_response('main/persona.html', locals(), context_instance=RequestContext(request))