# Django Imports
from django.urls import path
from django.views.decorators.cache import cache_page

# Project Imports
from .views import ObtenerPeliculaSerie, MostrarPeliculaSerie


urlpatterns = [
    path(
        route='',
        view=cache_page(60 * 15)(ObtenerPeliculaSerie.as_view()),
        name='index',
    ),
    path(
        route='movies/<movser>/',
        name='movie_serie',
        view=cache_page(60 * 15)(MostrarPeliculaSerie.as_view())
    ),
]
