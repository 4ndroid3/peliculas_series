""" Models de: Persona y Casting """
# Django Imports
from django.db import models


class Persona(models.Model):
    """ Modelo de la clase persona, que representa a los actores
    y directores que serán registrados en las peliculas y series.
    Campos:
    - nombre_apellido: charfield
    - img_persona: image
    - director: boolean
    - id_imdb: charfield
    """

    nombre_apellido = models.CharField(
        blank=False,
        max_length=100,
        verbose_name='Nombre y Apellido',
        help_text='Nombre y Apellido de la persona',
    )
    img_persona = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text='Imagen de la persona',
        verbose_name='Imagen',
    )
    director = models.BooleanField(
        default=False,
        verbose_name='Es Director',
        help_text='Identifica si la persona es director',
    )
    id_imdb = models.CharField(
        max_length=25,
        unique=True,
        blank=True,
        null=True,
        verbose_name='ID IMDb',
        help_text='ID unico de IMDb',
    )

    def __str__(self):
        return str(self.nombre_apellido)

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
