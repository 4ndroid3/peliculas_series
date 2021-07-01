# Django Imports
from django.urls import path
from django.views.decorators.cache import cache_page

# Project Imports
from .views import ObtenerPeliculaSerie, MostrarPeliculaSerie, NoLogueado


urlpatterns = [
    path(
        route='',
        view=ObtenerPeliculaSerie.as_view(),#cache_page(60 * 15, key_prefix='main')(ObtenerPeliculaSerie.as_view()),
        name='index',
    ),
    path(
        route='movies/<movser>/',
        name='movie_serie',
        view=cache_page(60 * 15)(MostrarPeliculaSerie.as_view())
    ),
    path(
        route='notlogged',
        view=cache_page(60 * 15, key_prefix='nologueado')(NoLogueado.as_view()),
        name='index',
    ),
]
