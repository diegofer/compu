# -*- coding: utf-8 -*-
from django.db import models
from .choices import ICON 


class Persona(models.Model):

	CLIENTE   = 'cliente'#'0'
	TECNICO   = 'tecnico'#'1'
	
	TIPO_PERSONA = (
		(CLIENTE, 'Cliente'),
	    (TECNICO, 'Técnico'),
	)
	
	nombre    = models.CharField(max_length=40)
	apellido  = models.CharField(max_length=40)
	cedula    = models.CharField(max_length=20, unique=True)
	direccion = models.CharField(max_length=255)
	telefono  = models.CharField(max_length=15)
	email     = models.EmailField(max_length=255, unique=True)
	tipo      = models.CharField(max_length=50, choices=TIPO_PERSONA)
	

	def __unicode__(self):
		return "%s %s" %(self.nombre, self.apellido)

	def _get_full_name(self):
		"Returns the person's full name."
		return '%s %s' % (self.nombre, self.apellido)
	full_name = property(_get_full_name)



class TipoServicio(models.Model):
	nombre = models.CharField(max_length=50)
	icon   = models.CharField(max_length=20, choices=ICON)

	def __unicode__(self):
		return self.nombre


		
class Marca(models.Model):
	nombre = models.CharField(max_length=50, unique=True)

	def __unicode__(self):
		return self.nombre


class Servicio(models.Model):

	EN_COLA        = 'en-cola'#'0'
	EN_REVISION    = 'en-revision'#'1'
	REPARADO       = 'reparado'#'1'
	ENTREGADO      = 'entregado'
	
	ESTADO = (
		(EN_COLA, 'En Cola'),
	    (EN_REVISION, 'En Revision'),
	    (REPARADO, 'Reparado'),
	    (ENTREGADO, 'Entregado'),
	)

	cliente    = models.ForeignKey(Persona)
	tipo       = models.ForeignKey(TipoServicio)
	marca      = models.ForeignKey(Marca)
	modelo     = models.CharField(max_length=50, blank=True, null=True)
	serial     = models.CharField(max_length=50, blank=True, null=True)
	created    = models.DateTimeField(auto_now_add = True) 
	updated    = models.DateTimeField(auto_now = True)
	estado     = models.CharField(max_length=12, choices=ESTADO, default=EN_COLA)

	def __unicode__(self):
		return "%s de %s" %( self.tipo.nombre, self.cliente.nombre )

