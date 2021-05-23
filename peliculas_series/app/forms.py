# Django Imports
from django import forms
from django.forms.widgets import HiddenInput


class SeleccionarMovieForm(forms.Form):
    """ Form para seleccionar una pelicula vista
    y agregarla junto con sus datos a la DB """
    movie_id = forms.CharField(
        widget=forms.HiddenInput(
            attrs= {
                'value':'',
            }
        )
    )
    temporada = forms.IntegerField(
        widget=forms.NumberInput(
            attrs= {
                'class': 'form-control',
                'placeholder': 'Numero de la temporada',
                'value': "0",
            }
        )
    )