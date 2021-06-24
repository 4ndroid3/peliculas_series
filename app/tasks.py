from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Serie, Pelicula_Serie
from users.models import Vista

# IMDB Imports
from imdb import IMDb

@shared_task
def add(x, y):
    return x + y 

@shared_task
def datos_temporada(serie_id, serie_temporada, usuario):
    """agrega datos adicionales a las series,
    duracion y cantidad de capitulos"""
    ultima_vista = Vista.objects.filter(id_profile__id_users__username=usuario).last().id_pelicula_serie.id
    # Llamo a la DB de IMDb
    ia = IMDb()
    info_serie = ia.get_movie(serie_id)
    ia.update(info_serie,'episodes')
    # Traigo los episodios desde IMDB
    id_serie = Pelicula_Serie.objects.filter(id=ultima_vista).last().pelicula_serie.id_serie.id
    serie = Serie.objects.filter(id=id_serie).last()
    serie.temporada_duracion = int(info_serie['runtimes'][0]) * len(info_serie['episodes'][serie_temporada])
    serie.cant_cap = len(info_serie['episodes'][serie_temporada])

    serie.save()

    return 'Update OK'