from fabric.api import * 
from fabric.contrib.console import confirm
from fabric.colors import green, red, yellow

import os
import re

RUTA_PROYECTO = os.path.join(os.path.dirname(os.path.abspath(__file__)))

STYLUS_PATH = 'main/static/main/css/stylus/'
STYLUS_FILE = 'main/static/main/css/stylus/style.styl' 




def initial_data():
	local('./manage.py dumpdata --indent=4 --exclude=main --exclude=south --exclude=auth.permission --exclude=contenttypes --exclude=admin.logentry --exclude=sessions  > usuarios/fixtures/initial_data.json')


################ COMANDOS STYLUS  ################

def watch_stylus(): 
	with lcd(STYLUS_PATH):
		local('stylus -w -o ../  %s' % STYLUS_FILE)


def actualizar():
	git_pull()


################ COMANDOS GIT  ################
def git_pull():
	local('git pull')