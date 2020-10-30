from django import forms
from .models import *
from sanitizer.forms import SanitizedCharField


class MessageForm(forms.ModelForm):
    '''
    Форма для чата
    '''
    message = SanitizedCharField(strip=False)

    class Meta:
        model = Message
        fields = '__all__'
        # exclude = ['author', 'recipient', 'timestamp', 'is_readed']
        #fields = ('message',)#, 'image_message', 'file_message')


class ChatForm(forms.ModelForm):
    '''
    Форма для создания нового чата
    '''
    class Meta:
        model = Chat
        fields = ('group_name', 'members', 'image_chat')
