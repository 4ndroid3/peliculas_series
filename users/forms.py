# Django Imports
from django import forms
from django.contrib.auth.forms import UsernameField, AuthenticationForm, UserCreationForm

# Project Imports
from users.models import User


class CustomLoginForm(AuthenticationForm):
    """ Form destinada a el sitema de
    login de usuario """
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
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

class CustomSigninForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
      model = User
      fields = ('email','username', 'password1', 'password2',)