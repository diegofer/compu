# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.urlresolvers import reverse
from datetime import datetime
import json



from crispy_forms.utils import render_crispy_form
from jsonview.decorators import json_view
from reportlab.pdfgen import canvas

from termcolor import colored
import fabfile as f

from main.models import Servicio, Persona
from main.forms import LoginForm, ServicioForm, PersonaForm, TipoServicioForm, MarcaForm, ComponenteForm, ServicioTecnicoForm




def home(request, estado='reciente'):

	loginForm = LoginForm()

	if request.method == 'POST':

		loginForm = LoginForm(data=request.POST)
		if loginForm.is_valid():
			username  = loginForm.cleaned_data['username']
			password  = loginForm.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None and user.is_active:
				login(request, user)
				return redirect('/')



	if estado == 'reciente':
		servicios = Servicio.objects.all().order_by('-updated')[:20]
	else:
		servicios = Servicio.objects.filter(estado__exact=estado)
		

	num_total     = Servicio.objects.all().count()	
	num_cola      = Servicio.objects.filter(estado__exact=Servicio.EN_COLA).count()
	num_revision  = Servicio.objects.filter(estado__exact=Servicio.EN_REVISION).count()
	num_reparado  = Servicio.objects.filter(estado__exact=Servicio.REPARADO).count()
	num_entregado = Servicio.objects.filter(estado__exact=Servicio.ENTREGADO).count()

	loginForm         = loginForm
	servicioForm      = ServicioForm()
	personaForm       = PersonaForm()
	tipoServicioForm  = TipoServicioForm()
	marcaForm         = MarcaForm()
	componenteForm    = ComponenteForm()

	ctx = {
		'loginForm': loginForm, 'SERVICIO': Servicio, 'estado': estado,
		'servicios': servicios, 
		'num_total':num_total, 'num_cola': num_cola, 'num_revision': num_revision, 'num_reparado': num_reparado, 'num_entregado': num_entregado,
		'servicioForm': servicioForm, 'personaForm': personaForm, 'tipoServicioForm': tipoServicioForm, 'marcaForm': marcaForm, 'componenteForm': componenteForm,
	}

	#if not request.user.is_authenticated():

	return render(request,'main/home.html', ctx)

def hacer_logout(request):
	logout(request)
	return redirect('/')		


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
	servicioTecnicoForm = ServicioTecnicoForm()

	return render_to_response('main/servicio.html', locals(), context_instance=RequestContext(request))




def persona(request, id):
	persona = Persona.objects.get(id=id)
	servicios = Servicio.objects.filter(cliente__pk=persona.id).order_by('-created')
	return render_to_response('main/persona.html', locals(), context_instance=RequestContext(request))



def actualizar(request):
	f.actualizar()  # corrocomando actualizar en fabfile
	

def imprimir(request):
	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

	# Create the PDF object, using the response object as its "file."
	p = canvas.Canvas(response)

	# Draw things on the PDF. Here's where the PDF generation happens.
	# See the ReportLab documentation for the full list of functionality.
	p.drawString(100, 100, "Hello world.")

	# Close the PDF object cleanly, and we're done.
	p.showPage()
	p.save()
	return response




######## OPERACIONES CRUD #############

@json_view
def guardar_servicio(request):
	datos = request.POST.copy() # le saco una copia al POST para poderlo editar
	datos['plazo'] = datetime.strptime(request.POST['plazo'], Servicio.DATA_TIME_FORMAT) # convierto mi custom datetime a un formato que entienda el fieldmodel

	form = ServicioForm(datos or None)

	if form.is_valid():
		new_servicio = form.save(commit=False)
		new_servicio.estado = Servicio.EN_COLA
		new_servicio.save()
		form.save_m2m()
		return {'success': True, 'url': new_servicio.get_absolute_url()}
	print colored(form.errors, "red", attrs=['bold'])
	form_html = render_crispy_form(form, context=RequestContext(request))
	return {'success': False, 'form_html': form_html}


@json_view
def guardar_servicio_tecnico(request):
	servicio = Servicio.objects.get(pk=request.POST['id_servicio'])
	form = ServicioTecnicoForm(request.POST or None, instance=servicio)

	if request.POST['tecnico']:
		
		if form.is_valid():
			servicio = form.save()
			return {'success': True, 'tecnico': servicio.tecnico.full_name, 'url_tecnico': servicio.tecnico.get_absolute_url() }
		print form.errors 
	form_html = render_crispy_form(form, context=RequestContext(request))
	return {'success': False, 'form_html': form_html, 'id_servicio': servicio.id}


@json_view
def guardar_servicio_estado(request):
	estado       = request.POST['estado']
	servicio_id  = request.POST['servicio_id']

	servicio = Servicio.objects.get(pk=servicio_id)
	servicio.estado = estado
	servicio.save(update_fields=['estado', 'updated'])

	return {'success': True, 'estado':servicio.estado}



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
        return {'success': True, 'value': tipo.id, 'nombre': tipo.nombre,}

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