# Django Imports
from django import forms
from django.contrib.auth.forms import UsernameField, AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    """ Form destinada a el sitema de
    login de usuario """
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)


    # user_email = forms.EmailField(
    #     widget=forms.EmailInput(
    #         attrs={
    #             'class': 'form-control',
    #         }
    #     )
    # )

    # usr_password = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             'class': 'form-control',
    #         }
    #     )
    # )

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        strip=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'current-password',
            }
        )
    )


    