from django.views.generic import TemplateView, ListView, DetailView, FormView
from users.models import Vista
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView


class MostrarPerfilUsuario(LoginRequiredMixin, TemplateView):
    """Resumen del Perfil de Usuario Logueado,
    Muestra datos personales de la persona.
    Cuantas peliculas vio? Cuantas temporadas?
    Tiempo total visto por la persona, (tiempo de series,
    tiempo de peliculas)
    Pequeño resumen con los generos que más mira el usuario.
    """
    template_name = 'users/perfil.html'


class MostrarViewsUsuario(LoginRequiredMixin, ListView):
    """Lista de las Peliculas / Series que vio
    el perfil. Posibilidad de ver la lista filtrada
    por varias condiciones.
    """
    model = Vista
    template_name = "users/lista.html"

    def get_ordering(self):
        """Return the field or fields to use for ordering the queryset."""
        self.ordering = "-fecha_vista"
        return self.ordering


class DetallePeliculaSerie(LoginRequiredMixin, DetailView):
    """Muestra el detalle e informacion detallada 
    de una pelicula vista"""
    model = Vista
    template_name = "users/detalle.html"


class MostrarEstadisticaUsuario(LoginRequiredMixin, TemplateView):
    """ Muestra las estadisticas del usuario
    como: cantidad de peliculas vistas, series vistas
    top de directores, top de actores, cantidad de hs
    por mes, por año, promedios, etc"""

    template_name = 'users/estadisticas.html'

class LoginUser(LoginView):
    """ View de Login personalizado"""
    template_name = 'registro/login.html'


class LogoutUser(LogoutView):
    """ View de LogOut Personalizado"""
    template_name = 'registro/logged_out.html'