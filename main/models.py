# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta

from termcolor import colored

from .choices import ICON 


class Persona(models.Model):
	
	nombre    = models.CharField(max_length=40)
	apellido  = models.CharField(max_length=40)
	cedula    = models.CharField(max_length=20, unique=True)
	direccion = models.CharField(max_length=255)
	telefono  = models.CharField(max_length=15)
	email     = models.EmailField(max_length=255, unique=True, blank=True)	

	def __unicode__(self):
		return "%s %s" %(self.nombre, self.apellido)

	def _get_full_name(self):
		return '%s %s' % (self.nombre, self.apellido)
	full_name = property(_get_full_name)

	def get_absolute_url(self):
		return reverse('main.views.persona', args=[str(self.id)])



class TipoServicio(models.Model):
	nombre = models.CharField(max_length=50, unique=True)
	icon   = models.CharField(max_length=20, choices=ICON)

	def __unicode__(self):
		return self.nombre


		
class Marca(models.Model):
	nombre = models.CharField(max_length=50, unique=True)

	def __unicode__(self):
		return self.nombre



class Componente(models.Model):
	nombre = models.CharField(max_length=50, unique=True)
	icon   = models.CharField(max_length=20, choices=ICON)

	def __unicode__(self):
		return self.nombre
	


class Servicio(models.Model):

	DATA_TIME_FORMAT = '%d-%m-%Y  %I %p'
	PLAZO_VENCIDO = 111

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

	cliente     = models.ForeignKey(Persona)
	tipo        = models.ForeignKey(TipoServicio)
	marca       = models.ForeignKey(Marca)
	modelo      = models.CharField(max_length=50, blank=True)
	serial      = models.CharField(max_length=50, blank=True)
	motivo      = models.TextField()
	componentes = models.ManyToManyField(Componente, blank=True, null=True, verbose_name=u'viene con')
	tecnico     = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
	empleado    = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='empleado_de', blank=True, null=True)
	created     = models.DateTimeField(auto_now_add = True) 
	updated     = models.DateTimeField(auto_now = True)
	estado      = models.CharField(max_length=12, choices=ESTADO, default=EN_COLA, blank=True)
	plazo       = models.DateTimeField(default=datetime.now, blank=True)

	def __unicode__(self):
		return "%s de %s" %( self.tipo.nombre, self.cliente.nombre )

	def get_absolute_url(self):
		return reverse('main.views.servicio', args=[str(self.id)])


	def _plazo_porcentaje(self):
		n = datetime.utcnow()			
		c = self.created
		p = self.plazo

		now    = datetime(n.year, n.month, n.day, n.hour, n.minute)
		creado = datetime(c.year, c.month, c.day, c.hour, c.minute)
		plazo  = datetime(p.year, p.month, p.day, p.hour, p.minute)

		if now < plazo:
			delta_rango = (plazo-creado).total_seconds() # 100%
			delta_van   = (now-creado).total_seconds()   # porcentaje completado

			result = (abs(delta_van) * 100) / abs(delta_rango)    # abs() retorna valores absolutos...
			return int(result)

		return self.PLAZO_VENCIDO

		
	percent = property(_plazo_porcentaje)