from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
  
    url(r'^$', 'main.views.home', name='home'),
    url(r'^(?P<estado>[-\w]+)/$', 'main.views.home', name='home'),

    #url(r'^servicios/(?P<estado>[-\w]+)/$', 'main.views.servicios', name='servicios'),
)