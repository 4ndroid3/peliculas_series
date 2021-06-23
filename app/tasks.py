from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Serie

# IMDB Imports
from imdb import IMDb

@shared_task
def add(x, y):
    return x + y 

@shared_task
def datos_temporada(serie_id, serie_temporada):
    """agrega datos adicionales a las series,
    duracion y cantidad de capitulos"""
    # Llamo a la DB de IMDb
    ia = IMDb()
    info_serie = ia.get_movie(serie_id)
    ia.update(info_serie,'episodes')
    # Traigo los episodios desde IMDB
    serie = Serie.objects.get(id_serie_)
    serie = Serie(
        temporada_duracion = int(
            info_serie['runtimes'][0]) * len(info_serie['episodes'][serie_temporada]),
        cant_cap=len(info_serie['episodes'][serie_temporada])
    )

    serie.save()

    return 'puton'