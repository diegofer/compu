# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.urlresolvers import reverse
from datetime import datetime
import json



from crispy_forms.utils import render_crispy_form
from jsonview.decorators import json_view
#from reportlab.pdfgen import canvas para generar pdf

from termcolor import colored
#import fabfile as f

from main.models import *
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

    ctx = {'loginForm':loginForm, 'SERVICIO':Servicio, 'estado': estado}

    if estado == 'reciente':
        ctx['servicios'] = Servicio.objects.all().order_by('-updated')[:20]
    else:
        ctx['servicios'] = Servicio.objects.filter(estado__exact=estado)
    
    try:
        ctx['estadistica'] = Estadistica.objects.latest()
    except Estadistica.DoesNotExist:
        ctx['estadistica'] = None
    
    if request.user.is_authenticated():
        ctx['servicioForm']      = ServicioForm()
        ctx['personaForm']       = PersonaForm()
        ctx['tipoServicioForm']  = TipoServicioForm()
        ctx['marcaForm']         = MarcaForm()
        ctx['componenteForm']    = ComponenteForm()

    return render(request,'main/home.html', ctx)



def hacer_logout(request):
    logout(request)
    return redirect('/')        


def servicio(request, id):
    loginForm = LoginForm()

    ctx = {'loginForm':loginForm, 'SERVICIO':Servicio}

    ctx['servicio']    = Servicio.objects.get(id=id)
    ctx['componentes'] = ctx['servicio'].componentes.all()

    try:
        ctx['estadistica'] = Estadistica.objects.latest()
    except Estadistica.DoesNotExist:
        ctx['estadistica'] = None

    if request.user.is_authenticated():
        ctx['servicioForm']        = ServicioForm(instance=ctx['servicio'])
        ctx['servicioTecnicoForm'] = ServicioTecnicoForm()
        ctx['personaForm']         = PersonaForm()
        ctx['tipoServicioForm']    = TipoServicioForm()
        ctx['marcaForm']           = MarcaForm()
        ctx['componenteForm']      = ComponenteForm()

    return render(request, 'main/servicio.html', ctx)




def persona(request, id):
    loginForm = LoginForm()
    persona = Persona.objects.get(id=id)
    servicios = Servicio.objects.filter(cliente__pk=persona.id).order_by('-created')
    return render(request, 'main/persona.html', locals())


######## ACTUALIZAR APP #############

@json_view
def actualizar(request):
    import os
    from threading import Timer

    if request.get_host() == '127.0.0.1:8000':
        return {'success':False, 'msg': 'No puedes actualizar desde el servidor de desarrollo: %s' % request.get_host()}

    os.chdir(os.path.dirname(os.path.dirname(__file__)))

    gitpull        = getstatusoutput('git pull')
    requirements   = getstatusoutput('pip install -r requirements_prod.txt')
    collectstatic  = getstatusoutput('python manage.py collectstatic --noinput')
    syncdb         = getstatusoutput('python manage.py syncdb')
    migrate        = getstatusoutput('python manage.py migrate')

    if os.name == 'nt':
        t = Timer(1.0, reloadApache)
        t.start()
    return {'success':True, 'msg': 'aplicacion actualizada, reiniciando el servidor...', 'output_git':gitpull, 'output_collectstatic':collectstatic}
  

def reloadApache():
    getstatusoutput('net stop Apache && net start Apache')

def getstatusoutput(cmd): 
    """Return (status, output) of executing cmd in a shell."""
    """This new implementation should work on all platforms."""
    import subprocess
    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, universal_newlines=True)  
    output = "".join(pipe.stdout.readlines()) 
    sts = pipe.returncode
    if sts is None: sts = 0
    return sts, output 



######## OPERACIONES CRUD #############

@json_view
def guardar_servicio(request):
    datos = request.POST.copy() # le saco una copia al POST para poderlo editar
    datos['plazo'] = datetime.strptime(request.POST['plazo'], Servicio.DATA_TIME_FORMAT) # convierto mi custom datetime a un formato que entienda el fieldmodel
    print colored(request.POST, 'yellow')

    if request.POST['id_servicio']:  # Verifico que haya un Id y si lo hay es porque hay que editar y no agregar un nuevo modelo
        servicio = Servicio.objects.get(pk=request.POST['id_servicio'])
        form = ServicioForm(datos or None, instance=servicio)
    else:
        form = ServicioForm(datos or None)

    if form.is_valid():
        new_servicio = form.save(commit=False)
        new_servicio.empleado = request.user
        new_servicio.estado = Servicio.EN_COLA
        new_servicio.save()
        form.save_m2m()
        registrar_estadisticas() # registro estadistacas en base de datos
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
            return {'success': True, 'tecnico': servicio.tecnico.get_full_name(), 'url_tecnico': servicio.tecnico.get_absolute_url() }
        print form.errors 
    form_html = render_crispy_form(form, context=RequestContext(request))
    return {'success': False, 'form_html': form_html, 'id_servicio': servicio.id}


@json_view
def guardar_servicio_estado(request):
    estado       = request.POST['estado']
    servicio_id  = request.POST['servicio_id']

    servicio = Servicio.objects.get(pk=servicio_id)
    servicio.estado = estado

    # guardamos fecha de entrega del servicio
    if estado == Servicio.ENTREGADO:
        servicio.entregado = datetime.now()
    else:
       servicio.entregado = None 
    
    servicio.save(update_fields=['estado', 'updated','entregado'])

    registrar_estadisticas() # registro estadistacas en base de datos

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





############# UTILES #################


def registrar_estadisticas():
    """ cuando creamos o actualizamos un servicio, creamos un registro en Estadistica """
    total        = Servicio.objects.all().count()
    en_cola      = Servicio.objects.filter(estado=Servicio.EN_COLA).count()
    en_revision  = Servicio.objects.filter(estado=Servicio.EN_REVISION).count()
    reparados    = Servicio.objects.filter(estado=Servicio.REPARADO).count()
    entregados   = Servicio.objects.filter(estado=Servicio.ENTREGADO).count()

    e = Estadistica(total=total, en_cola=en_cola, en_revision=en_revision, reparados=reparados, entregados=entregados)
    e.save()