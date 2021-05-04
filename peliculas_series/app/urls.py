# Django Imports
from django.urls import path

# Project Imports
from .views import ObtenerPelicula

urlpatterns = [
    path(
        route = '',
        view = ObtenerPelicula.as_view(),
        name = 'index',
    ),
    path(
        route = '<movser>/',
        view = ObtenerPelicula.as_view(),
        name = 'index',
    ),
]