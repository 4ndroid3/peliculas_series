""" Admin de la App 'users' """

# Django Imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Project Imports
from .models import User, Profile, Vista


class CustomUserAdmin(UserAdmin):
    """Configuración del admin modificado"""

    list_display = ('email', 'username', 'first_name', 'last_name',)
    list_filter = ('is_staff', )


class CustomProfileAdmin(admin.ModelAdmin):
    """ Configuracion de Muestra de Profiles en Admin"""
    list_display = ('id_users', 'peliculas_reg', 'series_reg',)


class CustomVistaAdmin(admin.ModelAdmin):
    """ Configuracion de Muestra de Vista de peliculas / series en el admin """
    list_display = ('id_profile', 'id_pelicula_serie', 'fecha_vista',)
    list_filter = ('id_profile', )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, CustomProfileAdmin)
admin.site.register(Vista, CustomVistaAdmin)
