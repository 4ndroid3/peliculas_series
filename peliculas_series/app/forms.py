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
    """
    año = forms.CharField(
        widget=forms.HiddenInput(
            attrs= {
                'value':'',
            }
        )
    )
    duracion = forms.CharField(
        widget=forms.HiddenInput(
            attrs= {
                'value':'',
            }
        )
    )
    puntaje = forms.CharField(
        widget=forms.HiddenInput(
            attrs= {
                'value':'',
            }
        )
    )
    generos = forms.CharField(
        widget=forms.HiddenInput(
            attrs= {
                'value':'',
            }
        )
    )
    imagen = forms.CharField(
        widget=forms.HiddenInput(
            attrs= {
                'value':'',
            }
        )
    )
    director = forms.CharField(
        widget=forms.HiddenInput(
            attrs= {
                'value':'',
            }
        )
    )
    casting = forms.CharField(
        widget=forms.HiddenInput(
            attrs= {
                'value':'',
            }
        )
    )
    movie_id = forms.CharField(
        widget=forms.HiddenInput(
            attrs= {
                'value':'',
            }
        )
    )"""