from fabric.api import * 
from fabric.contrib.console import confirm
from fabric.colors import green, red, yellow

import os
import re

RUTA_PROYECTO = os.path.join(os.path.dirname(os.path.abspath(__file__)))


####################################################
##              SERVIDOR DE PRODUCCION            ##
####################################################
COMPUCLINICA_PATH   = 'home/diego/compuclinica/compu'
IMPRETINTAS_PATH    = 'home/diego/impretintas/compu'

def actualizar_github():
	local('git add . && git commit -a')
	local('git push origin master')









################ COMANDOS DJANGO  ################
def initial_data():
	local('./manage.py dumpdata --indent=4 --exclude=main --exclude=south --exclude=auth.permission --exclude=contenttypes --exclude=admin.logentry --exclude=sessions  > usuarios/fixtures/initial_data.json')

def dumpdata_group():
	local(django_manage('./manage.py dumpdata --indent=4 --natural auth.Group > main/fixtures/initial_data.json'))

def django_manage(command='help', virtualenv='compu'):
	return "/bin/bash -l -c 'source /usr/local/bin/virtualenvwrapper.sh && workon %s && %s '" %(virtualenv, command)