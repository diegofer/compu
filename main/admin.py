# -*- coding: utf-8 -*-
from django.contrib import admin

from main.models import Persona, TipoServicio, Marca, Componente, Servicio, Estadistica
from usuarios.models import Usuario


class ServicioAdmin(admin.ModelAdmin):
    
    
    def save_model(self, request, obj, form, change):
        """ cuando creamos o actualizamos un servicio, creamos un registro en Estadistica """
        total        = Servicio.objects.all().count()
        en_cola      = Servicio.objects.filter(estado=Servicio.EN_COLA).count()
        en_revision  = Servicio.objects.filter(estado=Servicio.EN_REVISION).count()
        reparados    = Servicio.objects.filter(estado=Servicio.REPARADO).count()
        entregados   = Servicio.objects.filter(estado=Servicio.ENTREGADO).count()

        e = Estadistica(total=total, en_cola=en_cola, en_revision=en_revision, reparados=reparados, entregados=entregados)
        e.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tecnico":
            kwargs["queryset"] = Usuario.objects.filter(tipo__in=[Usuario.TECNICO,Usuario.ADMIN])
        return super(ServicioAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        

class EstadisticaAdmin(admin.ModelAdmin):
    list_display    = ('id', 'created', 'total', 'en_cola', 'en_revision', 'reparados', 'entregados')
    readonly_fields = ('total', 'en_cola', 'en_revision', 'reparados', 'entregados')
    



admin.site.register(Persona)
admin.site.register(TipoServicio)
admin.site.register(Marca)
admin.site.register(Componente)
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Estadistica, EstadisticaAdmin)