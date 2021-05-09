""" Views de la app principal """

# Django Imports
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import FormView

# Project Imports
from .models import Pelicula_Serie
from .forms import SeleccionarMovieForm

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

class MostrarPeliculaSerie(FormView):
    """ Al seleccionar una pelicula de la lista dada en ObtenerPeliculaSerie
    muestra la informacion completa de la pelicula"""
    template_name = 'inicio/movie_info.html'
    form_class = SeleccionarMovieForm
    success_url = '/'

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
                'casting': search['cast'][0:6],
                'id': search.getID()
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
                'casting': search['cast'][0:4],
                'id': search.getID()
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
        # import pdb; pdb.set_trace()

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            self.agregar_pelicula_serie(form.cleaned_data)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    
    def agregar_pelicula_serie(self, form):
        form['movie_id']