# Django Imports
from django.urls import path

# Project Imports
from .views import (MostrarPerfilUsuario,
                    MostrarViewsUsuario,
                    DetallePeliculaSerie,
                    MostrarEstadisticaUsuario,
                    LoginUser,
                    LogoutUser,
                    SignInUser)

urlpatterns = [
    path(
        route='perfil',
        view=MostrarPerfilUsuario.as_view(),
        name='profile',
    ),
    path(
        route='perfil/vistas',
        view=MostrarViewsUsuario.as_view(),
        name='list',
    ),
    path(
        route='perfil/vistas/<int:pk>',
        view=DetallePeliculaSerie.as_view(),
        name='detail',
    ),
    path(
        route='perfil/estadisticas/',
        view=MostrarEstadisticaUsuario.as_view(),
        name='detail',
    ),
    path(
        route='login/',
        view=LoginUser.as_view(),
        name='login'
    ),
    path(
        route='logout/',
        view=LogoutUser.as_view(),
        name='logout'
    ),
    path(
        route='signin/',
        view=SignInUser.as_view(),
        name='signin'
    ),
]
