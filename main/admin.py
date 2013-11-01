# -*- coding: utf-8 -*-
from django.contrib import admin
from main.models import Persona, TipoServicio, Marca, Servicio

admin.site.register(Persona)
admin.site.register(TipoServicio)
admin.site.register(Marca)
admin.site.register(Servicio)