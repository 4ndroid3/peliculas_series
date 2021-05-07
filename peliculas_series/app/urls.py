# Django Imports
from django.urls import path

# Project Imports
from .views import ObtenerPeliculaSerie, MostrarPeliculaSerie

urlpatterns = [
    path(
        route = '',
        view = ObtenerPeliculaSerie.as_view(),
        name = 'index',
    ),
    path(
        route = '<movser>/',
        view = ObtenerPeliculaSerie.as_view(),
        name = 'index',
    ),
    path(
        route = 'movies/<movser>/',
        view = MostrarPeliculaSerie.as_view(),
        name = 'movie_serie',
    ),
]