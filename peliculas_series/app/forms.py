# Django Imports
from django import forms


class SeleccionarMovieForm(forms.Form):
    """ Form para seleccionar una pelicula vista
    y agregarla junto con sus datos a la DB """
    movie_id = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                'value': '',
            }
        )
    )
    temporada = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Numero de la temporada',
                'value': "0",
            }
        )
    )
    fecha_vista = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Ej: 28/10/1990',
            }
        )
    )
    review = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Breve reseña de lo visto',
            }
        )
    )