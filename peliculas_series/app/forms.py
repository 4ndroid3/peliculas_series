# Django Imports
from django import forms
from django.forms.widgets import HiddenInput


class SeleccionarMovieForm(forms.Form):
    """ Form para seleccionar una pelicula vista
    y agregarla junto con sus datos a la DB """
    movie_id = forms.CharField(
        widget=forms.HiddenInput(
            attrs= {
                'class':'form-control',
                'value':'',
            }
        )
    )