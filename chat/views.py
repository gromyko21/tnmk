from django.shortcuts import render, redirect, reverse, get_list_or_404, get_object_or_404
from .models import *
from accounts.models import Profile
from .forms import MessageForm, ChatForm
from django.http import HttpResponseNotFound
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json
from django.db.models import Count


@login_required
def new_chat(request):
    if request.method == 'POST':
        new_chat_form = ChatForm(request.POST, request.FILES)
        if new_chat_form.is_valid():
            new_chat_form.instance.creater = request.user
            new_chat_form.save()
            return redirect('chat_url')
        else:
            HttpResponseNotFound("<h2>Введены неверные данные</h2>")
    else:
        new_chat_form = ChatForm()
    return render(request, 'chat/new_chat.html',
                  {'new_chat': new_chat_form,
                   'username': mark_safe(json.dumps(request.user.username)),
                   })


#Обновить данные чата
@login_required
def update_chat(request, id):
    chat = Chat.objects.get(pk=id)
    if request.method == "POST":
        chat_form = ChatForm(request.POST, request.FILES, instance=chat)
        chat.group_name = request.POST.get("group_name")
        chat.image_chat = request.POST.get('image_chat')
        # chat.members = chat.members.set(members)
        chat.author = request.user
        chat_form.save()
        chat.save()
        return redirect("chat_url")
    else:
        chat_form = ChatForm(instance=chat)
        return render(request, "chat/edit_chat.html",
                      {
                          "chat": chat,
                          'chat_form': chat_form,
                       })


# Перечисление всех чатов
@login_required
def chat(request):
    search_chats = request.GET.get('search_chats', '')
    if search_chats:
        body_chat = Chat.objects.order_by('-pk').filter\
            (members=request.user).filter(Q(members__profile__first_name__icontains=search_chats) | Q(members__profile__last_name__icontains=search_chats))
    else:
        body_chat = Chat.objects.filter(members=request.user).order_by('-pk')
    # body_chat = body_chat.order_by('-received_messages')

    for chat in body_chat:
        chat_id = get_object_or_404(Chat, id=chat.id)
        message = Message.objects.order_by('-pk').filter(recipient=chat_id)[0:1]
        chat.message = message
    #     # Получаем количество получателей в комнате
    #     # Чтобы решить личный чат это или беседа
        count = Chat.objects.filter(id=chat_id.id).annotate(Count('members'))
        count = count[0].members__count
        chat.count = count
        if count >= 2:
            if request.user == body_chat:
                # a = count.received_messages.members[0].profile.first_name
                a = body_chat
                return a

    return render(request, 'chat/dialogs.html',
                  {
                   'body_chat': body_chat,
                   # 'members': body_chat.members.all[1],
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

    if request.method == 'POST':
        message_form = MessageForm(request.POST, request.FILES)
        if message_form.is_valid():
            message_form.instance.author = request.user
            message_form.instance.recipient = list_users
            message_form.save()
        else:
            pass
    else:
        message_form = MessageForm()

    return render(request, 'chat/private_chat.html', {
                                              'message_form': message_form,
                                              'list_users': list_users.members.all,
                                              'room_name_json': mark_safe(json.dumps(id)),
                                              'image_message': mark_safe(json.dumps(str(Message.image_message))),
                                              'username': mark_safe(json.dumps(request.user.username)),
                                              # 'image_message': json.dumps(str(Message.image_message)) # py3
                                              })


# Загрузка фотографий в личных сообщениях
def upload_private_chat(request):
    if request.method == 'POST':
        message_form = MessageForm(request.POST, request.FILES)
        if message_form.is_valid():
            message_form.instance.author = request.user_id
            message_form.instance.recipient = request.room_id
            message_form.save()
        else:
            pass
    else:
        message_form = MessageForm()
    return render(request, 'chat/private_chat.html', {
                                              'message_form': message_form})
