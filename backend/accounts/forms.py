from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import CustomUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]