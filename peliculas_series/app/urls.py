# Django Imports
from django.urls import path

# Project Imports
from .views import ObtenerPeliculaSerie

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
]