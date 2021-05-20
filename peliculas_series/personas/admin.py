""" admin de la app personas """
# Django Imports
from django.contrib import admin

# Project Imports
from .models import Persona

class CustomPersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre_apellido','director', )
    list_filter = ('nombre_apellido', 'director')

admin.site.register(Persona, CustomPersonaAdmin)