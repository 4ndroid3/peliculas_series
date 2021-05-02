""" Models de: Persona y Casting """
# Django Imports
from django.db import models

class Persona(models.Model):
    """ Modelo de la clase persona, que representa a los actores
    y directores que serán registrados en las peliculas y series.
    
    Campos:
    - nombre: charfield
    - apellido: charfield
    - img_persona: image
    - director: boolean
    """

    nombre = models.CharField(
        blank = False,
        max_length = 50,
        verbose_name = 'Nombre',
        help_text = 'Nombre de la persona',
    )
    apellido = models.CharField(
        blank = False,
        max_length = 50,
        verbose_name = 'Apellido',
        help_text = 'Apellido de la persona',
    )
    img_persona = models.ImageField(
        upload_to = 'persona_img', 
        blank = True,
        null=True,
        help_text = 'Imagen de la persona',
        verbose_name = 'Imagen',
    )
    director = models.BooleanField(
        default = False,
        verbose_name = 'Es Director',
        help_text = 'Identifica si la persona es director',
    )

    def __str__(self):
        return str(self.nombre, ' ', self.apellido)
    
    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'

class Casting(models.Model):
    """ Grupo de personas que conforman el casting
    de una pelicula o serie

    Campos:
    - id_persona: FK
    """
    id_persona = models.ForeignKey(
        Persona,
        on_delete = models.CASCADE,
        blank = True,
        null = True,
        verbose_name = 'Actriz o Actor',
        help_text = 'Actriz o actor que conforman el casting de una pelicula',
    )

    def __str__(self):
        return str(self.id_persona)
    
    class Meta:
        verbose_name = 'Castgin'
        verbose_name_plural = 'Castings'