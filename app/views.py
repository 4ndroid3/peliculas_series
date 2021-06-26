""" Views de la app principal """

# Django Imports
from django.views.generic import TemplateView
from django.views.generic import FormView

# Project Imports
from .models import Pelicula_Serie, Serie, Pelicula, Tipo, Genero
from users.models import Vista, Profile
from personas.models import Persona
from .forms import SeleccionarMovieForm
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

# Tareas Asincronas
from app import tasks

# IMDB Imports
from imdb import IMDb

# Redis Imports
from django.views.decorators.cache import cache_page


class ObtenerPeliculaSerie(TemplateView):
    """ Clase principal para busqueda de peliculas o series
    esta tiene una funcion principal 'buscar_imdb' que realiza
    las busquedas con la API de IMDb, luego devuelve con un get
    lo encontrado, filtrando solo las peliculas y las series.
    """

    CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
    template_name = 'inicio/index.html'

    def buscar_imdb(self, peli_serie):
        """ Funcion para buscar una peli/serie en IMDB
        devuelve una lista con los nombres que coinciden """
        ia = IMDb()
        search = ia.search_movie(peli_serie)[0:14]
        list_search = []

        # Search me devuelve todas las peliculas encontradas en IMDB
        for peli_o_serie in search:

            # Filtro para que solo me muestre series y peliculas
            if (peli_o_serie['kind'] == 'tv series') or (peli_o_serie['kind'] == 'movie'):
                try:
                    list_search += [
                        [
                            peli_o_serie['title'],
                            peli_o_serie['year'],
                            peli_o_serie['cover url'],
                            peli_o_serie.getID()
                        ]
                    ]
                except:
                    list_search += [
                        ['Error en IMDB']
                    ]
        return list_search

    @cache_page(CACHE_TTL)
    def get(self, request, *args, **kwargs):
        try:
            busqueda = request.GET['search']
            context = self.get_context_data(**kwargs)
            context['busqueda'] = self.buscar_imdb(busqueda)
        except:
            context = self.get_context_data(**kwargs)

        return self.render_to_response(context)


class MostrarPeliculaSerie(FormView):
    """ Al seleccionar una pelicula de la lista dada
    en 'ObtenerPeliculaSerie' muestra la informacion completa de la pelicula,
    con la funcion 'traer_imdb' que se llama en el 'get' me muestra una
    pelicula/serie seleccionada y luego en el 'post' llama a la funcion
    'agregar_pelicula_serie' que realiza el agregado de informacion a la DB"""

    template_name = 'inicio/movie_info.html'
    form_class = SeleccionarMovieForm
    success_url = '/'

    def traer_imdb(self, id_peli_serie):
        """ funcion que trae una pelicula/serie cuando
        se le pasa como parametro un numero de ID"""
        ia = IMDb()
        search = ia.get_movie(id_peli_serie)

        # Armo una lista con los Objetos Persona, luego los paso
        # a str para poder presentarlos en el Template de casting
        casting = []
        for cast in search['cast'][0:5]: casting.append(cast['name'])
        casting = ', '.join(casting)

        # Hay algunas series que no tienen
        # 'runtimes' entonces atrapo el error.
        try:
            duracion = search['runtimes'][0]
        except KeyError:
            duracion = ''

        # Cuando IMDB busca una serie, esta no
        # tiene director, entonces se la separa con el IF.
        if search['kind'] != 'movie':
            info_peli_serie = {
                'tipo': search['kind'],
                'titulo': search['title'],
                'año': search['year'],
                'duracion': duracion,
                'puntaje': search['rating'],
                'generos': ', '.join(search['genres']),
                'imagen': search['full-size cover url'],
                'seasons': str(search['number of seasons']),
                'id': search.getID(),
                'casting': casting,
            }
        else:
            # Armo una lista con los Objetos Persona, luego los paso
            # a str para poder presentarlos en el template de director
            director = []
            for dir in search['director'][0:5]: director.append(dir['name'])
            director = ', '.join(director)

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

    @cache_page(CACHE_TTL)
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
            self.agregar_pelicula_serie(request, form.cleaned_data)
            return self.form_valid(form)
        else:
            print('invalid form')
            return self.form_invalid(form)

    def agregar_pelicula_serie(self, request, form):
        """
        Recibo el ID de la pelicula dsde el form del front.
        Con el ID busco toda la informacion que va a ir a la DB,
        primero compruebo de que no esté en la DB, si no está
        procedo a ir agregando los datos, filtrandolos de acuerdo
        si están en la DB o no, una vez comprobado los datos, los
        agrego en las vistas del usuario que esté logueado."""

        ia = IMDb()
        peli_o_serie = ia.get_movie(form['movie_id'])

        # Si la peli / serie no está en la DB
        # debo agregar todos los datos
        try:
            # En caso de ser una serie, hago un doble chekeo ya que las series
            # las puedo agregar de nuevo para cargar una temporada
            if form['temporada'] != 0:  # si la temporada es 0, es una pelicula
                peli_en_db = Pelicula_Serie.objects.get(
                    pelicula_serie__id_serie__temporada_nro=form['temporada'],
                    id_imdb=form['movie_id']
                ).id_imdb
            else:
                peli_en_db = Pelicula_Serie.objects.get(
                    id_imdb=form['movie_id']
                ).id_imdb
        except:
            peli_en_db = ''

        if form['movie_id'] != peli_en_db:
            # Si es una pelicula tiene directores.
            if peli_o_serie['kind'] == 'movie':
                # Busco director por director para ver si está en la DB
                for director in peli_o_serie['director']:
                    try:
                        persona_en_db = Persona.objects.get(
                            id_imdb=director.getID()
                        ).id_imdb
                    except:
                        persona_en_db = ''

                    if director.getID() != persona_en_db:
                        # La persona no se encuentra en la DB
                        # asique se la agrega
                        agregar_persona = Persona(
                            nombre_apellido=director['name'],
                            director=True,
                            id_imdb=director.getID()
                        )
                        agregar_persona.save()
            # Busco actor por actor para ver si está en la DB
            for actor in peli_o_serie['cast'][0:5]:
                try:
                    persona_en_db = Persona.objects.get(
                        id_imdb=actor.getID()
                    ).id_imdb
                except:
                    persona_en_db = ''

                if actor.getID() != persona_en_db:
                    # La persona no se encuentra en la DB
                    # asique se la agrega
                    agregar_persona = Persona(
                        nombre_apellido=actor['name'],
                        director=False,
                        id_imdb=actor.getID()
                    )
                    agregar_persona.save()
            # Busco genero por genero para ver si está en la DB
            for genero in peli_o_serie['genres']:
                try:
                    genero_en_db = Genero.objects.get(
                        tipo_genero=genero
                    ).tipo_genero
                except:
                    genero_en_db = ''

                if genero != genero_en_db:
                    agregar_genero = Genero(
                        tipo_genero=genero
                    )
                    agregar_genero.save()
            # Agrego pelicula o serie a la DB
            if peli_o_serie['kind'] == 'movie':
                # Si es una pelicula, agarra por esta rama
                pelicula = Pelicula(duracion=peli_o_serie['runtime'][0])
                pelicula.save()

                for pel in peli_o_serie['director']:
                    pelicula.director.add(Persona.objects.get(
                            nombre_apellido=pel
                        )
                    )
                    pelicula.save()
                # Agrego la clase tipo pelicula
                tipo = Tipo(id_pelicula=pelicula)
                tipo.save()

                # Agrego clase Pelicula_Serie a la DB
                pelicula_serie = Pelicula_Serie(
                    nombre=peli_o_serie['title'],
                    pelicula_serie=tipo,
                    año=peli_o_serie['year'],
                    puntaje_imdb=peli_o_serie['rating'],
                    img_portada=peli_o_serie['full-size cover url'],
                    id_imdb=peli_o_serie.getID()
                )

                pelicula_serie.save()

                # Agrego cada una de las personas del casting.
                for casting_pelicula in peli_o_serie['cast'][0:5]:
                    pelicula_serie.casting.add(Persona.objects.get(
                            nombre_apellido=casting_pelicula
                        )
                    )
                    pelicula_serie.save()
                # Agrego cada uno de los generos de la pelicula
                for genero_pelicula in peli_o_serie['genres']:
                    pelicula_serie.genero.add(Genero.objects.get(
                            tipo_genero=genero_pelicula
                        )
                    )
                    pelicula_serie.save()
            else:
                # Si es una serie, agarra por esta rama
                
                serie = Serie(temporada_nro=form['temporada'])
                serie.save()
                
                # Se pasan datos para agregar en forma 
                # asincrona los datos adicionales de las temporadas
                tasks.datos_temporada_asincronos.delay(
                    form['movie_id'], form['temporada'], serie.pk
                )

                # Agrego la clase tipo pelicula
                tipo = Tipo(id_serie=serie)
                tipo.save()

                # Agrego clase Pelicula_Serie a la DB
                pelicula_serie = Pelicula_Serie(
                    nombre=peli_o_serie['title'],
                    pelicula_serie=tipo,
                    año=peli_o_serie['year'],
                    puntaje_imdb=peli_o_serie['rating'],
                    img_portada=peli_o_serie['full-size cover url'],
                    id_imdb=peli_o_serie.getID()
                )

                pelicula_serie.save()

                # Agrego cada una de las personas del casting.
                for casting_serie in peli_o_serie['cast'][0:5]:
                    pelicula_serie.casting.add(Persona.objects.get(
                            nombre_apellido=casting_serie
                        )
                    )
                    pelicula_serie.save()
                # Agrego cada uno de los generos de la serie
                for genero_serie in peli_o_serie['genres']:
                    pelicula_serie.genero.add(Genero.objects.get(
                            tipo_genero=genero_serie
                        )
                    )
                    pelicula_serie.save()
        
        # Agrego la pelicula vista al usuario logueado
        usuario_logueado = Profile.objects.get(id_users=request.user)

        if form['temporada'] == 0:
            pelicula_serie_vista = Pelicula_Serie.objects.get(id_imdb=form['movie_id'])
        else:
            pelicula_serie_vista = Pelicula_Serie.objects.get(
                pelicula_serie__id_serie__temporada_nro=form['temporada'],
                id_imdb=form['movie_id']
            )

        registrar_vista = Vista(
            id_profile=usuario_logueado,
            id_pelicula_serie=pelicula_serie_vista,
            fecha_vista=str(form['fecha_vista']),
            review=form['review']
        )
        registrar_vista.save()
