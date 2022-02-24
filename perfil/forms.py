from dataclasses import fields
import email
from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User
from .models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput(), label='Senha')
    password2 = forms.CharField(required=False, widget=forms.PasswordInput(), label='Confirmação Senha')
    
    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password2', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        erro_forms = {}

        usuario_db = User.objects.get(username=data['username'])
        email_db = User.objects.get(email=data['email'])

        print(usuario_db)
        print(data['username'])

        if self.usuario:
            if usuario_db:
                if self.cleaned_data['username'] != usuario_db.username:
                    erro_forms['username'] = 'Usuário já existe'

            if email_db:
                if self.cleaned_data['email'] != email_db.email:
                    erro_forms['email'] = 'Email já existe'

            if self.cleaned_data['password']:
                if self.cleaned_data['password'] != self.cleaned_data['password2']:
                    erro_forms['password'] = 'As senhas não batem'
                    erro_forms['password2'] = 'As senhas não batem'

                if len(self.cleaned_data['password']) < 6:
                    erro_forms['password'] = 'A senha está muito curta, precisa ter pelo menos 6 caracteres.'

        else:
            print('Entrei')
            if usuario_db.username == cleaned['username']:
                print('entrei no error do usuario')
                erro_forms['username'] = 'O usuário já existe'
                return 

            if email_db.email == cleaned['email']:
                erro_forms['email'] = 'O Email já existe'

            if len(cleaned['password']) < 6:
                erro_forms['password'] = 'A senha possui menos de 6 caracteres'

            if not cleaned['password'] or not cleaned['password2']:
                erro_forms['password'] = 'Esse campo é obrigatório'

            if cleaned['password'] != cleaned['password2']:
                erro_forms['password'] = 'As senhas não conferem'

        if erro_forms:
            raise ValidationError(erro_forms)

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
        exclude = ('usuario',)

