# -*- coding: utf-8 -*-
from django.contrib import admin
from main.models import Persona, TipoServicio, Marca, Componente, Servicio

admin.site.register(Persona)
admin.site.register(TipoServicio)
admin.site.register(Marca)
admin.site.register(Componente)
admin.site.register(Servicio)