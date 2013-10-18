# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm #, UserCreationForm
from django.conf import settings


def home(request):
	return render_to_response('main/home.html', context_instance=RequestContext(request))
