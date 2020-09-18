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


class ChatForm(forms.ModelForm):
    '''
    Форма для создания нового чата
    '''

    class Meta:
        model = Chat
        fields = ('group_name', 'members', 'image_chat')
