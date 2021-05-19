""" Views de la app principal """

# Django Imports
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import FormView

# Project Imports
from .models import Pelicula_Serie, Serie, Pelicula, Tipo, Genero
from users.models import Vista, User, Profile
from personas.models import Persona
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

        # Armo una lista con los Objetos Persona, luego los paso a str
        casting = []
        for cast in search['cast'][0:5]: casting.append(cast['name'])
        casting = ', '.join(casting)

        director = []
        #for dir in search['director']: director = ', '.join(dir['name'])
        for dir in search['director'][0:5]: director.append(dir['name'])
        director = ', '.join(director)

        # Cuando IMDB busca una serie, esta no 
        # tiene director, entonces se la separa con el IF.

        if search['kind'] != 'movie':
            info_peli_serie = {
                'tipo': search['kind'],
                'titulo': search['title'],
                'año': search['year'],
                'puntaje': search['rating'],
                'generos': search['genres'],
                'imagen': search['full-size cover url'],
                'seasons': str(search['seasons']),
                'id': search.getID(),
                'casting': casting,
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
                'director': director,
                'id': search.getID(),
                'casting': casting,
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
            print('invalid form')
            return self.form_invalid(form)

    
    def agregar_pelicula_serie(self, form):
        """
        Recibo el ID de la pelicula dsde el form del front.
        Con el ID busco toda la informacion que va a ir a la DB
        """
        info_peli_serie = self.traer_imdb(form['movie_id'])
        #person.getfullsizeURL()
        

        import pdb; pdb.set_trace()