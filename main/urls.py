from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
  
    url(r'^$', 'main.views.home', name='home'),
    url(r'^(?P<estado>[-\w]+)/$', 'main.views.home', name='home'),
    url(r'^servicio/(\d+)/$', 'main.views.servicio', name='servicio' ),
    url(r'^persona/(\d+)/$', 'main.views.persona', name='persona' ),
)