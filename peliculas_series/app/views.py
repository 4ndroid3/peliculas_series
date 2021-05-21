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

        # Armo una lista con los Objetos Persona, luego los paso 
        # a str para poder presentarlos en el Template, de casting
        # y director
        casting = []
        for cast in search['cast'][0:5]: casting.append(cast['name'])
        casting = ', '.join(casting)

        director = []
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
                'generos': ', '.join(search['genres']),
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
        ia = IMDb()
        peli_o_serie = ia.get_movie(form['movie_id'])
        #import pdb; pdb.set_trace()
        # Si la peli / serie no está en la DB 
        # debo agregar todos los datos
        try:
            peli_en_db = Pelicula_Serie.objects.get(id_imdb=form['movie_id']).id_imdb
        except:
            peli_en_db = ''

        if form['movie_id'] != peli_en_db:
            # Busco director por director para ver si está en la DB
            for director in peli_o_serie['director']:
                try:
                    persona_en_db = Persona.objects.get(id_imdb=director.getID())
                except:
                    persona_en_db = ''

                if director.getID() != persona_en_db:
                    #import pdb; pdb.set_trace()
                    # La persona no se encuentra en la DB 
                    # asique se la agrega
                    persona = ia.get_person(director.getID())
                    agregar_persona = Persona(
                        nombre_apellido=persona['name'],
                        img_persona=persona.get_fullsizeURL(),
                        director=True,
                        id_imdb=persona.getID()
                    )
                    agregar_persona.save()
                else:
                    print('La persona ya está en la DB')
            
            # Busco actor por actor para ver si está en la DB
            for actor in peli_o_serie['cast'][0:2]:
                try:
                    persona_en_db = Persona.objects.get(id_imdb=actor.getID())
                except:
                    persona_en_db = ''

                if actor.getID() != persona_en_db:
                    # La persona no se encuentra en la DB 
                    # asique se la agrega
                    persona = ia.get_person(actor.getID())
                    agregar_persona = Persona(
                        nombre_apellido=persona['name'],
                        img_persona=persona.get_fullsizeURL(),
                        director=False,
                        id_imdb=persona.getID()
                    )
                    agregar_persona.save()
                else:
                    print('La persona ya está en la DB')

            # Busco genero por genero para ver si está en la DB
            for genero in peli_o_serie['genres']:
                try:
                    genero_en_db = Genero.objects.get(tipo_genero=genero)
                except:
                    genero_en_db = ''

                if genero != genero_en_db:
                    agregar_genero = Genero(
                        tipo_genero= genero
                    )
                    agregar_genero.save()
                else:
                    print('El genero ya está en la DB')
        else:
            print('La Pelicula ya está agregada a la BD')