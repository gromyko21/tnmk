from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    '''
    Комментарии к новостям на главной странице
    '''
    body = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ('body',)
