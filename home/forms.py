from django import forms
from django.contrib.auth.models import User
from .models import *

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Comment
        fields = ('body',)
