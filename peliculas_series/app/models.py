""" Models de: Pelicula_Serie, Serie, Pelicula, Tipo """

# Django Imports
from django.db import models

class Pelicula_Serie(models.Model):
    """
    Modelo de DB para la tabla de peliculas y series

    Campos:
    - pelicula_serie: FK
    - año: int
    - puntaje_imdb: float
    - genero: char
    - casting: FK
    - img_portada: image
    """

    pelicula_serie = models.ForeignKey(
        'app.models.Tipo',
        on_delete = models.CASCADE,
        help_text = 'Es una pelicula o una serie?',
        verbose_name = 'Pelicula / Serie', 
    )
    año = models.PositiveIntegerField(
        max_length = 4,
        blank = True,
        null=True,
        help_text = 'Año en que se publico el libro.',
        verbose_name = 'Año de publicación',
    )
    puntaje_imdb = models.DecimalField(
        max_digits = 2,
        decimal_places = 1,
        blank = True,
        null = True,
        help_text = 'Puntaje de la pagina IMDb',
        verbose_name = 'Puntaje IMDb',
    )
    genero = models.CharField(
        max_length = 25,
        blank = True,
        null = True,
        verbose_name = 'Genero',
        help_text = 'Genero de la pelicula o serie',
    )
    casting = models.OneToOneField(
        'personas.models.Casting',
        on_delete = models.CASCADE,
        help_text = 'Casting de la pelicula o serie',
        verbose_name = 'Casting',
    )
    img_portada = models.ImageField(
        upload_to = 'portada_img', 
        blank = True,
        null=True,
        help_text = 'Imagen de portada de la pelicula o serie',
        verbose_name = 'Portada',
    )

    def __str__(self):
        return str(self.pelicula_serie)
    
    class Meta:
        verbose_name = 'Pelicula o Serie'
        verbose_name_plural = 'Peliculas o Series'

class Tipo(models.Model):
    """ Clase intermedia para manejar si es pelicula o serie """
    id_serie = models.OneToOneField(
        'app.models.Serie',
        on_delete = models.CASCADE,
        blank = True,
        null = True,
    )
    id_pelicula = models.OneToOneField(
        'app.models.Pelicula',
        on_delete = models.CASCADE,
        blank = True,
        null = True,
    )

    def __str__(self):
        return str(self.id_pelicula, self.id_serie)

class Serie(models.Model):
    """ Modelo que maneja el ingreso de series a la DB 
    
    Campos:
    - temporada_nro: integer
    - temporada_duracion: duration
    - cant_cap: integer
    """
    temporada_nro = models.PositiveIntegerField(
        max_digits = 2,
        blank = True,
        help_text = 'Numero de la temporada',
        verbose_name = 'Temporada Numero',
    )
    temporada_duracion = models.DurationField(
        blank = True,
        verbose_name = 'Duración',
        help_text = 'Tiempo de duracion de la temporada completa',
    )
    cant_cap = models.PositiveIntegerField(
        max_digits = 2,
        blank = True,
        help_text = 'Cantidad de capitulos de la temporada',
        verbose_name = 'Cantidad de capitulos',
    )

class Pelicula(models.Model):
    """ Modelo que maneja el ingreso de peliculas a la DB 
    
    Campos:
    - duracion: time
    - director: FK
    """
    director = models.ForeignKey(
        'personas.models.Persona',
        on_delete = models.CASCADE,
        blank = True,
        null = True,
        help_text = 'Director de la Pelicula',
        verbose_name = 'Director',
    )
    duracion = models.DurationField(
        blank = True,
        verbose_name = 'Duración',
        help_text = 'Tiempo de duración de la pelicula',
    )