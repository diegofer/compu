from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
  
  	url(r'^guardar_servicio/$', 'main.views.guardar_servicio', name='guardar_servicio' ),
    url(r'^$', 'main.views.home', name='home'),
    url(r'^(?P<estado>[-\w]+)/$', 'main.views.home', name='home'),
    url(r'^servicio/(\d+)/$', 'main.views.servicio', name='servicio' ),
    url(r'^persona/(\d+)/$', 'main.views.persona', name='persona' ),

    
)