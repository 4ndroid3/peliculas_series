from django.views.generic import TemplateView, ListView, DetailView, CreateView
from users.models import Vista
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect

# Forms Imports
from users.forms import CustomLoginForm, CustomSigninForm

# Project Imports
from users.models import User


class MostrarPerfilUsuario(LoginRequiredMixin, TemplateView):
    """Resumen del Perfil de Usuario Logueado,
    Muestra datos personales de la persona.
    Cuantas peliculas vio? Cuantas temporadas?
    Tiempo total visto por la persona, (tiempo de series,
    tiempo de peliculas)
    Pequeño resumen con los generos que más mira el usuario.
    """
    template_name = 'users/perfil.html'
    login_url = '/login/'


class MostrarViewsUsuario(LoginRequiredMixin, ListView):
    """Lista de las Peliculas / Series que vio
    el perfil. Posibilidad de ver la lista filtrada
    por varias condiciones.
    """
    model = Vista
    template_name = "users/lista.html"
    login_url = '/login/'

    def get_ordering(self):
        """Return the field or fields to use for ordering the queryset."""
        self.ordering = "-fecha_vista"
        return self.ordering


class DetallePeliculaSerie(LoginRequiredMixin, DetailView):
    """Muestra el detalle e informacion detallada
    de una pelicula vista"""
    model = Vista
    template_name = "users/detalle.html"
    login_url = '/login/'


class MostrarEstadisticaUsuario(LoginRequiredMixin, TemplateView):
    """ Muestra las estadisticas del usuario
    como: cantidad de peliculas vistas, series vistas
    top de directores, top de actores, cantidad de hs
    por mes, por año, promedios, etc"""

    template_name = 'users/estadisticas.html'
    login_url = '/login/'


class LoginUser(LoginView):
    """ View de Login personalizado"""

    template_name = 'registro/login.html'
    form_class = CustomLoginForm

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponseRedirect('/')


class LogoutUser(LogoutView):
    """ View de LogOut Personalizado"""
    template_name = 'registro/logged_out.html'

class SignInUser(CreateView):
    form_class = CustomSigninForm
    template_name = 'registro/create_user.html'
    queryset = User
    success_url = '/'
