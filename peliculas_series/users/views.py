from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from app.models import Pelicula_Serie
from users.models import Vista


class MostrarPerfilUsuario(TemplateView):
    """Resumen del Perfil de Usuario Logueado,
    Muestra datos personales de la persona.
    Cuantas peliculas vio? Cuantas temporadas?
    Tiempo total visto por la persona, (tiempo de series,
    tiempo de peliculas)
    Pequeño resumen con los generos que más mira el usuario.
    """
    template_name = 'users/perfil.html'


class MostrarViewsUsuario(ListView):
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

class DetallePeliculaSerie(DetailView):
    model = Vista
    template_name = "users/detalle.html"


class MostrarEstadisticaUsuario(TemplateView):
    template_name = 'users/estadisticas.html'