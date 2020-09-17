from django.shortcuts import render, redirect, reverse, get_list_or_404, get_object_or_404
from .models import *
from accounts.models import Profile
from .forms import MessageForm, ChatForm
from django.http import HttpResponseNotFound
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json
from django.db.models import Sum
from django.db.models import Count
from django.db.models import Avg


@login_required
def new_chat(request):
    if request.method == 'POST':
        new_chat_form = ChatForm(request.POST)
        if new_chat_form.is_valid():
            new_chat_form.instance.creater = request.user
            #new_chat_form.instance.members.ste = request.user
            new_chat_form.save()
            return redirect('chat_url')
        else:
            HttpResponseNotFound("<h2>Введены неверные данные</h2>")
    else:
        new_chat_form = ChatForm()
    return render(request, 'chat/new_chat.html',
                  {'new_chat': new_chat_form})


#Перечисление всех чатов
@login_required
def chat(request):
    search_chats = request.GET.get('search_chats', '')
    if search_chats:
        chats = Profile.objects.order_by('-pk').filter(Q(first_name__icontains=search_chats) | Q(last_name__icontains=search_chats))
    else:
        chats = Profile.objects.order_by('-pk')
        #Получаем последнее сообщение
    body_chat = Chat.objects.order_by('-pk').filter(Q(members=request.user))

    for chat in body_chat:
        chat_id = get_object_or_404(Chat, slug=chat.slug)
        message = Message.objects.order_by('-pk').filter(Q(recipient=chat_id))[0:1]
        chat.message = message
        count = Chat.objects.filter(id=chat_id.id).aggregate(Count('members'))
        chat.count = count

    return render(request, 'chat/dialogs.html',
                  {'chat': body_chat,
                   })


# Страница личного чата
@login_required
def private_chat(request, slug):
    list_users = Chat.objects.filter(slug=slug)
    return render(request, 'chat/private_chat.html', {
                                              'list_users':list_users,
                                              'room_name_json': mark_safe(json.dumps(slug)),
                                              'username': mark_safe(json.dumps(request.user.username)),
                                              })
