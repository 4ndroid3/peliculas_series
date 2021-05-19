""" Models de: Pelicula_Serie, Serie, Pelicula, Tipo """

# Django Imports
from django.db import models

# Project Imports
from personas.models import Persona

class Serie(models.Model):
    """ Modelo que maneja el ingreso de series a la DB 
    
    Campos:
    - temporada_nro: integer
    - temporada_duracion: duration
    - cant_cap: integer
    """
    temporada_nro = models.PositiveIntegerField(
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
        blank = True,
        help_text = 'Cantidad de capitulos de la temporada',
        verbose_name = 'Cantidad de capitulos',
    )

    class Meta:
        verbose_name = 'Serie'
        verbose_name_plural = 'Series'

class Pelicula(models.Model):
    """ Modelo que maneja el ingreso de peliculas a la DB 
    
    Campos:
    - duracion: time
    - director: FK
    """
    director = models.ForeignKey(
        Persona,
        on_delete = models.CASCADE,
        blank = True,
        null = True,
        help_text = 'Director de la Pelicula',
        verbose_name = 'Director',
    )
    duracion = models.CharField(
        max_length = 50,
        blank = True,
        verbose_name = 'Duración',
        help_text = 'Tiempo de duración de la pelicula',
    )
    
    class Meta:
        verbose_name = 'Pelicula'
        verbose_name_plural = 'Peliculas'

class Tipo(models.Model):
    """ Clase intermedia para manejar si es pelicula o serie """
    id_serie = models.OneToOneField(
        Serie,
        on_delete = models.CASCADE,
        blank = True,
        null = True,
        default=''
    )
    id_pelicula = models.OneToOneField(
        Pelicula,
        on_delete = models.CASCADE,
        blank = True,
        null = True,
        default=''
    )
    def __str__(self):
        if self.id_pelicula != '':
            return str(self.id_pelicula)
        else:
            return str(self.id_serie)

class Genero(models.Model):
    tipo_genero= models.CharField(
        max_length = 50,
        unique= True,
        blank = True,
        null = True,
        verbose_name = 'Genero',
        help_text = 'Genero de la pelicula o serie',
    )

    def __str__(self):
        return str(self.tipo_genero)
    
    class Meta:
        verbose_name = 'Genero'
        verbose_name_plural = 'Generos'
    

class Pelicula_Serie(models.Model):
    """
    Modelo de DB para la tabla de peliculas y series

    Campos:
    - nombre: charfield
    - pelicula_serie: FK
    - año: int
    - puntaje_imdb: float
    - genero: char
    - casting: FK
    - img_portada: image
    - id_imdb
    """

    nombre = models.CharField(
        max_length = 50,
        verbose_name = 'Nombre',
        help_text = 'Nombre de la pelicula / serie',
    )

    pelicula_serie = models.ForeignKey(
        Tipo,
        on_delete = models.CASCADE,
        help_text = 'ID',
        verbose_name = 'Pelicula / Serie', 
    )
    año = models.PositiveIntegerField(
        blank = True,
        null=True,
        help_text = 'Año en que se estreno la pelicula/serie.',
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
    genero = models.ManyToManyField(
        Genero,
        blank=True,
        help_text = 'Genero de la pelicula o serie',
        verbose_name = 'Genero',
    )
    casting = models.ManyToManyField(
        Persona,
        blank=True,
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
    id_imdb = models.CharField(
        max_length = 25,
        blank = True,
        null = True,
        verbose_name = 'ID IMDb',
        help_text = 'ID unico de IMDb',
    )

    def __str__(self):
        return str(self.nombre)
    
    class Meta:
        verbose_name = 'Pelicula o Serie'
        verbose_name_plural = 'Peliculas o Series'

