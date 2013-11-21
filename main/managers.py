from django.contrib.auth.models import BaseUserManager

class UsuarioManager(BaseUserManager):
	
	def _create_user(self, email, dni, password, is_staff, is_superuser, **extra_fields):
		if not email:
			raise ValueError('El email debe ingresarse')
		email = self.normalize_email(email)
		user = self.model(email=email, dni=dni, is_active=True, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, dni, password=None, **extra_fields):
		return self._create_user(email, dni, password, False, False, **extra_fields)

	def create_superuser(self, email, dni, password, **extra_fields):
		return self._create_user(email, dni, password, True, True, **extra_fields)
	
