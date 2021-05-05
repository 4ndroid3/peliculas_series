""" Views de la app principal """

# Django Imports
from django.shortcuts import render
from django.views.generic import TemplateView

# Project Imports
from .models import Pelicula_Serie

# IMDB Imports
from imdb import IMDb ,IMDbError

class ObtenerPelicula(TemplateView):
    """ Clase principal para busqueda de peliculas o series
    y luego agregarlas a la db como vistas.
    """
    template_name = 'inicio/index.html'

    def buscar_imdb(self, peli_serie):
        """ Funcion para buscar una peli/serie en IMDB
        devuelve una lista con los nombres que coinciden """
        ia = IMDb()
        search = ia.search_movie(peli_serie)
        list_search = []
        for x in search:
            list_search += [[x['title'], x['year'], x['cover url']]]
        return list_search
    
    def get(self, request, *args, **kwargs):
        try:
            busqueda = kwargs['movser']            
        except:
            busqueda = kwargs['movser'] = ''
        context = self.get_context_data(**kwargs)
        context['busqueda'] = self.buscar_imdb(busqueda)
        return self.render_to_response(context)

        

