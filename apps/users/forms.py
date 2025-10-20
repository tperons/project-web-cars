from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        label='Primeiro nome',
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
        }))

    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
        })
    )

    password1 = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-control',
        })
    )

    password2 = forms.CharField(
        label='Confirmação',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-control',
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
        })
    )

    password = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-control',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'password')

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('A sua conta ainda não foi aprovada! Por favor, aguarde...', code='incative')
        super().confirm_login_allowed(user)
