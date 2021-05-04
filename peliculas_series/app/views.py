""" Views de la app principal """

# Django Imports
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import ListView

# Project Imports
from .models import Pelicula_Serie

# IMDB Imports
from imdb import IMDb ,IMDbError

class ObtenerPelicula(CreateView):
    """ Clase principal para busqueda de peliculas o series
    y luego agregarlas a la db como vistas.
    """

    model = Pelicula_Serie
    fields = ['nombre',]
    template_name = 'inicio/index.html'

    def buscar_imdb(self, peli_serie):
        """ Funcion para buscar una peli/serie en IMDB
        devuelve una lista con los nombres que coinciden """
        ia = IMDb()
        search = ia.search_movie(peli_serie)

        return search

    def get(self, request, *args, **kwargs):
        #import pdb; pdb.set_trace()
        """Si especifico en la URL el kwargs movser
        se da el try, en caso de que sea el menu principal 
        se da el except"""
        try:
            peli_serie = kwargs['movser']
        except:
            kwargs['movser'] = ''
            peli_serie = kwargs['movser']

        kwargs['busqueda'] = self.buscar_imdb(peli_serie)
        

        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        print(kwargs)
        """Insert the single object into the context dict."""
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        return super().get_context_data(**context)

        

