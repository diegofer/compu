# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, StrictButton, FieldWithButtons

from main.models import Servicio, Persona, TipoServicio, Marca

class ServicioForm(ModelForm):

	def __init__(self, *args, **kwargs):
		super(ServicioForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		#self.helper.form_action = '/guardar_servicio/'

		self.helper.form_id     = 'form-servicio'
		self.helper.form_class  = 'form-horizontal'
		self.helper.label_class = 'col-md-2'
		self.helper.field_class = 'col-md-8'

		self.helper.layout = Layout(
			FieldWithButtons('cliente', StrictButton("<i class='fa fa-plus fa-fw'></i>", css_id="cliente-btn")),
		    FieldWithButtons('tipo', StrictButton("<i class='fa fa-plus fa-fw'></i>", css_id="tipo-btn")),
		    FieldWithButtons('marca', StrictButton("<i class='fa fa-plus fa-fw'></i>", css_id="marca-btn")),
		    'modelo',
		    'serial',
		    'estado',		
		)

	class Meta:
		model = Servicio

class PersonaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.fields['nombre'].label = ""
        self.fields['apellido'].label = ""
        self.fields['cedula'].label = ""
        self.fields['direccion'].label = ""
        self.fields['telefono'].label = ""
        self.fields['email'].label = ""
        self.fields['tipo'].label = ""

        self.helper.form_id     = 'form-persona'
        self.helper.form_class  = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8 col-lg-offset-2'

        self.helper.layout = Layout(
        	PrependedText('nombre', "<i class='fa fa-user fa-fw'></i>", placeholder="nombre"),
        	PrependedText('apellido', "<i class='fa fa-user fa-fw'></i>", placeholder="apellido"),
        	PrependedText('cedula', "cc", placeholder="cedula"),
        	PrependedText('direccion', "<i class='fa fa-map-marker fa-fw'></i>", placeholder="direccion"),
        	PrependedText('telefono', "<i class='fa fa-phone fa-fw'></i>", placeholder="telefono"),
            PrependedText('email', "<i class='fa fa-envelope-o fa-fw'></i>", placeholder="email"),
        	PrependedText('tipo', "<i class='fa fa-group fa-fw'></i>", placeholder="tipo", data_placeholder="Elija tipo de persona..."),
        )
	

    class Meta:
        model = Persona
		


class TipoServicioForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TipoServicioForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.fields['nombre'].label = ""
        self.fields['icon'].label = ""

        self.helper.form_id     = 'form-tipo-servicio'
        self.helper.form_class  = 'form-horizontal'
        self.helper.field_class = 'col-lg-8 col-lg-offset-2'

        self.helper.layout = Layout(
            PrependedText('nombre', "<i class='fa fa-wrench fa-fw'></i>", placeholder="nombre"),
            PrependedText('icon', "<i class='fa fa-rocket fa-fw'></i>", placeholder="icono"),
        )
    

    class Meta:
        model = TipoServicio




class MarcaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MarcaForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.fields['nombre'].label = ""

        self.helper.form_id     = 'form-marca'
        self.helper.form_class  = 'form-horizontal'
        self.helper.field_class = 'col-lg-8 col-lg-offset-2'

        self.helper.layout = Layout(
            PrependedText('nombre', "<i class='fa fa-wrench fa-fw'></i>", placeholder="nombre"),
        )
    

    class Meta:
        model = Marca
        