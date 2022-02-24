from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from .models import *

class UserForm(forms.ModelForm):
    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario
    class Meta:
        model = Perfil
        fields = '__all__'
        exclude = ('usuario',)

class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'password', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data

