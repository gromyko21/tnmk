from django import forms
from .models import *


class MessageForm(forms.ModelForm):
    '''
    Форма для чата
    '''
    message = forms.CharField()

    class Meta:
        model = Message
        fields = ('message',)
