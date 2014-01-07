# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
  
  	url(r'^guardar_servicio/$', 'main.views.guardar_servicio', name='guardar_servicio' ),
  	url(r'^guardar_servicio_tecnico/$', 'main.views.guardar_servicio_tecnico', name='guardar_servicio_tecnico' ),
    url(r'^guardar_servicio_estado/$', 'main.views.guardar_servicio_estado', name='guardar_servicio_estado' ),
    	
    url(r'^actualizar/$', 'main.views.actualizar', name='actualizar' ),
    url(r'^hacer_logout/$', 'main.views.hacer_logout', name='hacer_logout' ),



  	url(r'^guardar_persona/$', 'main.views.guardar_persona', name='guardar_persona' ),
  	url(r'^guardar_tipo_servicio/$', 'main.views.guardar_tipo_servicio', name='guardar_tipo_servicio' ),
  	url(r'^guardar_marca/$', 'main.views.guardar_marca', name='guardar_marca' ),
  	url(r'^guardar_componente/$', 'main.views.guardar_componente', name='guardar_componente' ),

   
    url(r'^servicio/(\d+)/$', 'main.views.servicio', name='servicio' ),
    url(r'^persona/(\d+)/$', 'main.views.persona', name='persona' ),
    url(r'^usuario/(\d+)/$', 'main.views.usuario', name='usuario' ),
    

    url(r'^clientes/$', 'main.views.clientes', name='clientes' ),
    
    url(r'^search_cliente/$', 'main.views.search_cliente', name='search_cliente' ),
    url(r'^search_servicio/$', 'main.views.search_servicio', name='search_servicio' ),



    url(r'^$', 'main.views.home', name='home'),
    url(r'^(?P<estado>[-\w]+)/$', 'main.views.home', name='home'), 
)