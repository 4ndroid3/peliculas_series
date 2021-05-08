""" Views de la app principal """

# Django Imports
from django.shortcuts import render
from django.views.generic import TemplateView

# Project Imports
from .models import Pelicula_Serie

# IMDB Imports
from imdb import IMDb ,IMDbError

class ObtenerPeliculaSerie(TemplateView):
    """ Clase principal para busqueda de peliculas o series
    y luego agregarlas a la db como vistas.
    """
    template_name = 'inicio/index.html'

    def buscar_imdb(self, peli_serie):
        """ Funcion para buscar una peli/serie en IMDB
        devuelve una lista con los nombres que coinciden """
        ia = IMDb()
        search = ia.search_movie(peli_serie)[0:14]
        list_search = []
        for x in search:
            try:
                list_search += [[x['title'], x['year'], x['cover url'], x.getID()]]
            except:
                list_search += [['Error en IMDB']]
        return list_search
    
    def get(self, request, *args, **kwargs):
        try:
            busqueda = kwargs['movser']
            context = self.get_context_data(**kwargs)
            context['busqueda'] = self.buscar_imdb(busqueda)            
        except:
            context = self.get_context_data(**kwargs)
        
        return self.render_to_response(context)

class MostrarPeliculaSerie(TemplateView):
    """ Al seleccionar una pelicula de la lista dada en ObtenerPeliculaSerie
    muestra la informacion completa de la pelicula"""
    template_name = 'inicio/movie_info.html'

    def traer_imdb(self, id_peli_serie):
        """ funcion que trae una pelicula/serie cuando 
        se le pasa como parametro un numero de ID"""
        ia = IMDb()
        search = ia.get_movie(id_peli_serie)

        # Cuando IMDB busca una serie, esta no 
        # tiene director, entonces se la separa con el IF.
        if search['kind'] != 'movie':
            info_peli_serie = {
                'tipo': search['kind'],
                'titulo': search['title'],
                'año': search['year'],
                'duracion': search['runtime'][0],
                'puntaje': search['rating'],
                'generos': search['genres'],
                'imagen': search['full-size cover url'],
                'casting': search['cast'][0:6]
            }
        else:
            info_peli_serie = {
                'tipo': search['kind'],
                'titulo': search['title'],
                'año': search['year'],
                'duracion': search['runtime'][0],
                'puntaje': search['rating'],
                'generos': search['genres'],
                'imagen': search['full-size cover url'],
                'director': search['director'],
                'casting': search['cast'][0:4]
            }

        return info_peli_serie

    def get(self, request, *args, **kwargs):
        try:
            busqueda = kwargs['movser']
            context = self.get_context_data(**kwargs)
            context['busqueda'] = self.traer_imdb(busqueda)            
        except:
            context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

