""" admin de la app personas """
# Django Imports
from django.contrib import admin

# Project Imports
from .models import Persona, Casting

class CustomPersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'director', )
    list_filter = ('apellido', 'nombre', 'director')

class CustomCastingAdmin(admin.ModelAdmin):
    list_display = ('id_persona',)

admin.site.register(Persona, CustomPersonaAdmin)
admin.site.register(Casting, CustomCastingAdmin)