# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group


class UsuarioManager(BaseUserManager):
	
	def _create_user(self, email, dni, password, is_admin, is_superuser, **extra_fields):
		if not email:
			raise ValueError('El email debe ingresarse')
		email = self.normalize_email(email)
		user = self.model(email=email, dni=dni, is_active=True, is_admin=is_admin, is_superuser=is_superuser, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, dni, password=None, **extra_fields):
		return self._create_user(email, dni, password, False, False, **extra_fields)

	def create_superuser(self, email, dni, password, **extra_fields):
		return self._create_user(email, dni, password, True, True, **extra_fields)


def TIPO_USERS_FROM_GROUP():
	lista = Group.objects.only("name")
	TIPO = {}
	for name in lista:
	    TIPO[str(name.name)] = str(name.name)
	return TIPO.iteritems()



class Usuario(AbstractBaseUser, PermissionsMixin):

	ADMIN     = 'administrador'#'0'
	TECNICO   = 'tecnico'#'1'
	EMPLEADO  = 'empleado'
	
	TIPO_USUARIO = (
		(ADMIN, 'Administrador (a)'),
	    (TECNICO, 'Técnico'),
	    (EMPLEADO, 'Empleado (a)'),
	)

	email     = models.EmailField(unique=True)
	dni       = models.IntegerField(unique=True)
	tipo      = models.CharField(max_length=50, choices=TIPO_USUARIO) 
	nombre    = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=50)
	telefono  = models.CharField(max_length=15)

	is_active = models.BooleanField(default=True)
	is_admin  = models.BooleanField(default=False)

	objects   = UsuarioManager()
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['dni']

	def get_full_name(self):
		return self.email

	def get_short_name(self):
	    return self.email

	def get_absolute_url(self):
		return '/usuario/' #reverse('main.views.persona', args=[str(self.id)])

	def __unicode__(self):
		return self.email

	@property
	def is_staff(self):
	    return self.is_admin