from fabric.api import * 
from fabric.contrib.console import confirm
from fabric.colors import green, red, yellow

import os
import re

RUTA_PROYECTO = os.path.join(os.path.dirname(os.path.abspath(__file__)))

STYLUS_PATH = 'main/static/main/css/stylus/'
STYLUS_FILE = 'main/static/main/css/stylus/style.styl' 


################ COMANDOS STYLUS  ################

def watch_stylus(): 
	with lcd(STYLUS_PATH):
		local('stylus -w -o ../  %s' % STYLUS_FILE)


def actualizar():
	git_pull()


################ COMANDOS GIT  ################
def git_pull():
	local('git pull')