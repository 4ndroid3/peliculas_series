""" Models de: User, Profile y Vistas """

# Django Imports
from django.db import models
from django.contrib.auth.models import AbstractUser

# Project Imports
from app.models import Pelicula_Serie


class User(AbstractUser):
    """User Model Modificado
    Se extiende de la clase AbstractUser para agregar nuevas funcionalidades
    al usuario base.
    - Se edita el email, haciendo que sea unico, se agregan mensajes de error.
    - Se agrega el email como campo para loguearse.
    - Se agrega el usuario, nombre y apellido como usuarios requeridos.
    """

    email = models.EmailField(
        unique=True,
        error_messages={
            'Unico': 'Ya existe un usuario con esa dirección de Email'
        },
    )

    # USERNAME_FIELD me idica que el campo email ahora
    # me lo va a pedir para iniciar sesion.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_verified = models.BooleanField(
        'verified',
        default=True,
        help_text='True cuando el usuario verifico su cuenta vía email.'
    )

    def __str__(self):
        return str(self.username)


class Profile(models.Model):
    """Profile Model.
    Informacion informal del usuario,
    contiene un perfil con imagen, estadisticas y datos adicionales.
    Campos:
    - id_users: OneToOne
    - biografia: text
    - nacimiento: date
    - img_perfil: image
    - peliculas_reg: integer
    - series_reg: integer
    """
    id_users = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        help_text='Nombre del Usuario',
        verbose_name='Usuario',
    )
    biografia = models.TextField(
        max_length=500,
        blank=True,
        help_text='Breve resumen acerca tuyo',
        verbose_name='Biografía',
    )
    nacimiento = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de Nacimiento',
        help_text='Fecha en la que nació',
    )
    img_perfil = models.ImageField(
        upload_to='profile_img',
        blank=True,
        null=True,
        help_text='Imagen de perfil del usuario',
        verbose_name='Imagen de Perfil',
    )

    # Stats
    peliculas_reg = models.PositiveIntegerField(
        default=0,
        help_text='Cantidad de peliculas vistas',
        verbose_name='Peliculas vistas',
    )
    series_reg = models.PositiveIntegerField(
        default=0,
        help_text='Cantidad de series vistas',
        verbose_name='Series vistas'
    )

    def __str__(self):
        return str(self.id_users)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'


class Vista(models.Model):
    """ Registro de las peliculas / series vistas por el usuario
    Campos:
    - id_profile: FK
    - id_pelicula_serie: FK
    - fecha_vista: date
    - review: text
    """
    id_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        help_text='Nombre del Perfil',
        verbose_name='Nombre de Perfil',
    )
    id_pelicula_serie = models.ForeignKey(
        Pelicula_Serie,
        on_delete=models.CASCADE,
        help_text='Nombre de la pelicula vista',
        verbose_name='Nombre Pelicula / Serie',
    )
    fecha_vista = models.DateField(
        blank=True,
        null=True,
        verbose_name='Visto el',
        help_text='Fecha en la que se vió la pelicula',
    )
    review = models.TextField(
        max_length=500,
        default=' ',
        null=True,
        help_text='Breve resumen de la pelicula',
        verbose_name='Resumen',
    )

    def __str__(self):
        return str(self.id_pelicula_serie)

    class Meta:
        verbose_name = 'Vista'
        verbose_name_plural = 'Vistas'
