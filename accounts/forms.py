from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import *

#Ворма вхда
class UserLoginForm(AuthenticationForm):

    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'Uname'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'Uname'}))

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ()

#Форма для редактирования личного профиля
class ProfileForm(forms.ModelForm):

    image = forms.ImageField()

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'birth_date', 'image')

