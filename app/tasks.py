# Celery Imports
from __future__ import absolute_import, unicode_literals
from celery import shared_task

# Project Imports
from .models import Serie

# IMDB Imports
from imdb import IMDb


@shared_task
def datos_temporada_asincronos(serie_id, serie_temporada, pk_serie):
    """agrega datos adicionales a las series,
    duracion y cantidad de capitulos"""

    # Llamo a la DB de IMDb
    ia = IMDb()

    # Con el ID de la serie la vuelvo a buscar en IMDBpy
    info_serie = ia.get_movie(serie_id)

    # Se le pasa el filtro update, para que
    # traiga datos adicionales de series.
    ia.update(info_serie, 'episodes')

    # Actualizo la serie 'asincronamente'
    serie = Serie.objects.get(id=pk_serie)
    serie.temporada_duracion = int(
        info_serie['runtimes'][0]) * len(
            info_serie['episodes'][serie_temporada]
        )
    serie.cant_cap = len(info_serie['episodes'][serie_temporada])

    serie.save(update_fields=['temporada_duracion', 'cant_cap'])

    return 'Update OK'
