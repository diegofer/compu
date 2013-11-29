# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.utils.translation import ugettext, ugettext_lazy as _

from usuarios.models import Usuario



class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('email', 'dni',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = Usuario
        #fields = ['email', 'password', 'tipo', 'is_active', 'is_admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UsuarioAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'tipo', 'dni', 'is_admin', 'is_active',)
    list_filter = ('is_admin', 'is_active',)

    fieldsets = (
        ('Datos del Usuario', {'fields': ( ('nombre', 'dni',), ('apellidos', 'email',), 'telefono',)}),
        ('Ambito del Usuario', {'fields': ('tipo',  ('is_active', 'is_admin'), 'groups', )}), #'user_permissions')}),                                     
        ('Datos de Login y cambio de contraseña', {'fields': ('last_login', 'password')}),
    )
    readonly_fields = ('last_login', 'is_superuser', 'groups')


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'dni', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def queryset(self, request):
        qs = super(UsuarioAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.exclude(is_superuser=True) #qs.filter(Q(user_padre=request.user.id) | Q(id=request.user.id))

    def save_model(self, request, obj, form, change):
        
        obj.save()
        
        if change:
            tipo = obj.tipo
            g = Group.objects.get(name=tipo)
            obj.groups.clear()
            obj.groups.add(g)


admin.site.register(Usuario, UsuarioAdmin)