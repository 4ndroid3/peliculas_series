""" Admin de la app principal """

# Django Imports
from django.contrib import admin

# Project Imports
from .models import Pelicula_Serie, Tipo, Pelicula, Serie, Genero

class CustomPeliculaSerieAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'año', 'puntaje_imdb',)
    list_filter = ('nombre',)

class CustomTipoAdmin(admin.ModelAdmin):
    list_display = ('id_serie', 'id_pelicula',)

class CustomPeliculaAdmin(admin.ModelAdmin):
    list_display = ('duracion',)
    list_filter = ('director',)

class CustomSerieAdmin(admin.ModelAdmin):
    list_display = ('temporada_nro', 'temporada_duracion', 'cant_cap')

class CustomGeneroAdmin(admin.ModelAdmin):
    list_display = ('tipo_genero',)

admin.site.register(Pelicula_Serie, CustomPeliculaSerieAdmin)
admin.site.register(Tipo, CustomTipoAdmin)
admin.site.register(Pelicula, CustomPeliculaAdmin)
admin.site.register(Serie, CustomSerieAdmin)
admin.site.register(Genero, CustomGeneroAdmin)