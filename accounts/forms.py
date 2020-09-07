from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *


class UserLoginForm(AuthenticationForm):
    '''
    Форма для входа
    '''
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'Uname'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'Uname'}))


class ProfileForm(forms.ModelForm):
    '''
    Форма для редактирования личного профиля
    '''
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        exclude = ['user']
        fields = '__all__'


class PostForm(forms.ModelForm):
    '''
    Форма для записей на личной странице
    '''
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        exclude = ['author', 'post']
        fields = '__all__'

