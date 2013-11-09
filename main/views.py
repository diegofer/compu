# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm #, UserCreationForm
from django.conf import settings

from crispy_forms.utils import render_crispy_form
from jsonview.decorators import json_view

from main.models import Servicio, Persona
from main.forms import ServicioForm, PersonaForm, TipoServicioForm, MarcaForm, ComponenteForm


def home(request, estado='reciente'):
	if estado == 'reciente':
		servicios = Servicio.objects.all().order_by('-updated')[:20]
	else:
		servicios = Servicio.objects.filter(estado__exact=estado)

	num_total     = Servicio.objects.all().count()	
	num_cola      = Servicio.objects.filter(estado__exact=Servicio.EN_COLA).count()
	num_revision  = Servicio.objects.filter(estado__exact=Servicio.EN_REVISION).count()
	num_reparado  = Servicio.objects.filter(estado__exact=Servicio.REPARADO).count()
	num_entregado = Servicio.objects.filter(estado__exact=Servicio.ENTREGADO).count()

	SERVICIO = Servicio # estado es el model0 vacio para tener en la plantilla las variables estaticas..
	estado   = estado

	servicioForm      = ServicioForm()
	personaForm       = PersonaForm()
	tipoServicioForm  = TipoServicioForm()
	marcaForm         = MarcaForm()
	componenteForm    = ComponenteForm()

	
	return render_to_response('main/home.html', locals(), context_instance=RequestContext(request))



def servicio(request, id):
	servicio = Servicio.objects.get(id=id)
	componentes = servicio.componentes.all()

	num_total     = Servicio.objects.all().count()	
	num_cola = Servicio.objects.filter(estado__exact=Servicio.EN_COLA).count()
	num_revision = Servicio.objects.filter(estado__exact=Servicio.EN_REVISION).count()
	num_reparado = Servicio.objects.filter(estado__exact=Servicio.REPARADO).count()
	num_entregado = Servicio.objects.filter(estado__exact=Servicio.ENTREGADO).count()

	SERVICIO = Servicio # estado es el model0 vacio para tener en la plantilla las variables estaticas..
	
	servicioForm      = ServicioForm()
	personaForm       = PersonaForm()
	tipoServicioForm  = TipoServicioForm()
	marcaForm         = MarcaForm()
	componenteForm    = ComponenteForm()

	return render_to_response('main/servicio.html', locals(), context_instance=RequestContext(request))




def persona(request, id):
	persona = Persona.objects.get(id=id)
	servicios = Servicio.objects.filter(cliente__pk=persona.id).order_by('-created')
	return render_to_response('main/persona.html', locals(), context_instance=RequestContext(request))



######## OPERACIONES CRUD #############

@json_view
def guardar_servicio(request):
	form = ServicioForm(request.POST or None)

	if form.is_valid():
		new_servicio = form.save(commit=False)
		new_servicio.estado = Servicio.EN_COLA
		new_servicio.save()
		form.save_m2m()
		return {'success': True}
	print form.errors
	form_html = render_crispy_form(form, context=RequestContext(request))
	return {'success': False, 'form_html': form_html}


@json_view
def guardar_persona(request):
    form = PersonaForm(request.POST or None)
    
    if form.is_valid():
        persona = form.save()
        return {'success': True, 'value': persona.id, 'nombre': persona.full_name}

    form_html = render_crispy_form(form, context=RequestContext(request))
    return {'success': False, 'form_html': form_html}


@json_view
def guardar_tipo_servicio(request):
    form = TipoServicioForm(request.POST or None)
    
    if form.is_valid():
        tipo = form.save()
        return {'success': True, 'value': tipo.id, 'nombre': tipo.nombre}

    form_html = render_crispy_form(form, context=RequestContext(request))
    return {'success': False, 'form_html': form_html}


@json_view
def guardar_marca(request):
    form = MarcaForm(request.POST or None)
    
    if form.is_valid():
        marca = form.save()
        return {'success': True, 'value': marca.id, 'nombre': marca.nombre}

    form_html = render_crispy_form(form, context=RequestContext(request))
    return {'success': False, 'form_html': form_html}


@json_view
def guardar_componente(request):
    form = ComponenteForm(request.POST or None)

    if form.is_valid():
        componente = form.save()
        return {'success': True, 'value': componente.id, 'nombre': componente.nombre }
    print form.errors
    form_html = render_crispy_form(form, context=RequestContext(request))
    return {'success': False, 'form_html': form_html}