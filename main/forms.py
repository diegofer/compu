# -*- coding: utf-8 -*-
from django import forms

from django.forms import ModelForm, DateTimeField, DateTimeInput
from django.forms.widgets import PasswordInput, TextInput
from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm #, UserCreationForm
from django.utils.translation import ugettext as _
from datetime import datetime

from termcolor import colored

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Hidden
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, StrictButton, FieldWithButtons

from main.models import Servicio, Persona, TipoServicio, Marca, Componente


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'ingrese email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control','placeholder':'ingrese password'}))
        

class ServicioForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ServicioForm, self).__init__(*args, **kwargs)

        #self.fields['cliente'].queryset = Persona.objects.filter(tipo__exact=Persona.CLIENTE)
        self.helper = FormHelper(self)

        self.helper.form_id     = 'form-servicio'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-sm-offset-1 col-sm-2 '
        self.helper.field_class = 'col-sm-8 '

        self.helper.layout = Layout(
            PrependedText('plazo', "<i class='fa fa-calendar'></i>", css_class="input-sm"),
            FieldWithButtons('cliente', StrictButton("<i class='fa fa-plus fa-fw'></i>",  css_id="cliente-btn", css_class="btn-default btn-sm")),
            FieldWithButtons('tipo',    StrictButton("<i class='fa fa-plus fa-fw'></i>",  css_id="tipo-btn",    css_class="btn-default btn-sm")),
            FieldWithButtons('marca',   StrictButton("<i class='fa fa-plus fa-fw'></i>",  css_id="marca-btn",   css_class="btn-default btn-sm")),           
            Field('modelo', css_class="input-sm"),
            Field('serial', css_class="input-sm"),
            Field('motivo', rows="2", css_class='input-xlarge'),
            FieldWithButtons('componentes', StrictButton("<i class='fa fa-plus fa-fw'></i>", css_id="componentes-btn", css_class="btn-default")),      
            
        )

    class Meta:
        model = Servicio
        exclude = ['estado', 'tecnico']
        localized_fields = ('plazo',)
        widgets = {
            'plazo': DateTimeInput(format=Servicio.DATA_TIME_FORMAT),
        }


class ServicioTecnicoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ServicioTecnicoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.fields['tecnico'].label = ""

        #self.fields['tecnico'].queryset = Persona.objects.filter(tipo__exact=Persona.TECNICO)

        self.helper.form_id     = 'form-servicio-tecnico'


        self.helper.layout = Layout(
            'tecnico',
            Hidden('id_servicio', '{{servicio.id}}'),
            StrictButton('Asignar Tecnico', css_id="guardar-servicio-tecnico-btn", data_loading_text="Guardando...", css_class="btn-danger btn-block btn-lg"),
        )
    

    class Meta:
        model = Servicio
        fields = ['tecnico']
        

class PersonaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_show_labels = False
        self.helper.form_id     = 'form-persona'
        self.helper.form_class  = 'form-horizontal'
        self.helper.field_class = 'col-sm-8 col-sm-offset-2'

        self.helper.layout = Layout(
        	PrependedText('nombre', "<i class='fa fa-user fa-fw'></i>", placeholder="nombre"),
        	PrependedText('apellido', "<i class='fa fa-user fa-fw'></i>", placeholder="apellido"),
        	PrependedText('cedula', "cc", placeholder="cedula"),
        	PrependedText('direccion', "<i class='fa fa-map-marker fa-fw'></i>", placeholder="direccion"),
        	PrependedText('telefono', "<i class='fa fa-phone fa-fw'></i>", placeholder="telefono"),
            PrependedText('email', "<i class='fa fa-envelope-o fa-fw'></i>", placeholder="email"),
        )
	

    class Meta:
        model = Persona





class TipoServicioForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TipoServicioForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_show_labels = False
        self.helper.form_id     = 'form-tipo-servicio'
        self.helper.form_class  = 'form-horizontal'
        self.helper.field_class = 'col-sm-8 col-sm-offset-2'

        self.helper.layout = Layout(
            PrependedText('nombre', "<i class='fa fa-crosshairs'></i>", placeholder="nombre"),
            PrependedText('icon', "<i class='fa fa-rocket fa-fw'></i>", placeholder="icono"),
        )
    

    class Meta:
        model = TipoServicio




class MarcaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MarcaForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        
        self.helper.form_show_labels = False
        self.helper.form_id     = 'form-marca'
        self.helper.form_class  = 'form-horizontal'
        self.helper.field_class = 'col-sm-8 col-sm-offset-2'

        self.helper.layout = Layout(
            PrependedText('nombre', "<i class='fa fa-crosshairs'></i>", placeholder="nombre"),
        )
    

    class Meta:
        model = Marca



class ComponenteForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ComponenteForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_show_labels = False
        self.helper.form_id   = 'form-componente'
        self.helper.form_class = 'form-horizontal'
        self.helper.field_class  = 'col-sm-8 col-sm-offset-2'

        self.helper.layout = Layout(
            PrependedText('nombre', "<i class='fa fa-crosshairs'></i>", placeholder='nombre'),
            PrependedText('icon', "<i class='fa fa-puzzle-piece fa-fw'></i>", placeholder='icono'),           
        )

    class Meta:
        model = Componente
        
        
        