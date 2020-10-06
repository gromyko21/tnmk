from django.shortcuts import render, redirect, reverse, get_list_or_404, get_object_or_404
from .models import *
from accounts.models import Profile
from .forms import MessageForm, ChatForm
from django.http import HttpResponseNotFound
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json


@login_required
def new_chat(request):
    if request.method == 'POST':
        new_chat_form = ChatForm(request.POST)
        if new_chat_form.is_valid():
            new_chat_form.instance.creater = request.user
            new_chat_form.save()
            return redirect('chat_url')
        else:
            HttpResponseNotFound("<h2>Введены неверные данные</h2>")
    else:
        new_chat_form = ChatForm()
    return render(request, 'chat/new_chat.html',
                  {'new_chat': new_chat_form})


# Перечисление всех чатов
@login_required
def chat(request):
    search_chats = request.GET.get('search_chats', '')
    if search_chats:
        chats = Profile.objects.order_by('-pk').filter(Q(first_name=search_chats) | Q(last_name=search_chats))
    else:
        chats = Profile.objects.order_by('-pk')

    return render(request, 'chat/dialogs.html',
                  {
                   'room_name_json': mark_safe(json.dumps(request.user.id)),
                   'username': mark_safe(json.dumps(request.user.username)),
                   })


# Страница личного чата
@login_required
def private_chat(request, id):

    list_users = Chat.objects.get(id=id)
    # Нерпочитанные сообщения
    messages = Message.objects.filter(recipient=list_users)
    for message in messages:
        if request.user != message.author:
            message.is_readed = True
            message.save()

    return render(request, 'chat/private_chat.html', {
                                              'list_users': list_users.members.all,
                                              'room_name_json': mark_safe(json.dumps(id)),
                                              'username': mark_safe(json.dumps(request.user.username)),
                                              })

