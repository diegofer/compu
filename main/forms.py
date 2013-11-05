# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, StrictButton, FieldWithButtons

from main.models import Servicio, Persona

class ServicioForm(ModelForm):

	def __init__(self, *args, **kwargs):
		super(ServicioForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		self.helper.form_action = '/formulario/'

		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-2'
		self.helper.field_class = 'col-lg-8'
		self.helper.layout = Layout(
			FieldWithButtons('cliente', StrictButton("<i class='fa fa-plus fa-fw'></i>", css_id="cliente-btn")),
		    FieldWithButtons('tipo', StrictButton("<i class='fa fa-plus fa-fw'></i>", css_id="tipo-btn")),
		    FieldWithButtons('marca', StrictButton("<i class='fa fa-plus fa-fw'></i>", css_id="marca-btn")),
		    'modelo',
		    'serial',
		    'estado',
		    #StrictButton('save', css_class='btn-default'),	
		    
		    FormActions(
	            StrictButton('Guardar', css_class='btn-primary'),		
	        )  
	     
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
		self.fields['tipo'].label = ""

		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-2'
		self.helper.field_class = 'col-lg-8 '

		self.helper.layout = Layout(
			PrependedText('nombre', "<i class='fa fa-user fa-fw'></i>", placeholder="nombre"),
			PrependedText('apellido', "<i class='fa fa-user fa-fw'></i>", placeholder="apellido"),
			PrependedText('cedula', "cc", placeholder="cedula"),
			PrependedText('direccion', "<i class='fa fa-map-marker fa-fw'></i>", placeholder="direccion"),
			PrependedText('telefono', "<i class='fa fa-phone fa-fw'></i>", placeholder="telefono"),
			PrependedText('tipo', "<i class='fa fa-group fa-fw'></i>", placeholder="tipo"),
		)

		

	class Meta:
		model = Persona
		





 
class MessageForm(forms.Form):
    text_input = forms.CharField()
 
    textarea = forms.CharField(
        widget = forms.Textarea(),
    )
 
    radio_buttons = forms.ChoiceField(
        choices = (
            ('option_one', "Option one is this and that be sure to include why it's great"), 
            ('option_two', "Option two can is something else and selecting it will deselect option one")
        ),
        widget = forms.RadioSelect,
        initial = 'option_two',
    )
 
    checkboxes = forms.MultipleChoiceField(
        choices = (
            ('option_one', "Option one is this and that be sure to include why it's great"), 
            ('option_two', 'Option two can also be checked and included in form results'),
            ('option_three', 'Option three can yes, you guessed it also be checked and included in form results')
        ),
        initial = 'option_one',
        widget = forms.CheckboxSelectMultiple,
        help_text = "<strong>Note:</strong> Labels surround all the options for much larger click areas and a more usable form.",
    )
 
    appended_text = forms.CharField(
        help_text = "Here's more help text"
    )
 
    prepended_text = forms.CharField()
 
    prepended_text_two = forms.CharField()
 
    multicolon_select = forms.MultipleChoiceField(
        choices = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')),
    )
 
    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('text_input', css_class='input-xlarge'),
        Field('textarea', rows="3", css_class='input-xlarge'),
        'radio_buttons',
        Field('checkboxes', style="background: #FAFAFA; padding: 10px;"),
        AppendedText('appended_text', '.00'),
        PrependedText('prepended_text', '<input type="checkbox" checked="checked" value="" id="" name="">', active=True),
        PrependedText('prepended_text_two', '@'),
        'multicolon_select',
        FormActions(
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
            Submit('cancel', 'Cancel'),
        )
    )
