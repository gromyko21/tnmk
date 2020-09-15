from django.shortcuts import render, redirect, reverse, get_list_or_404, get_object_or_404
from .models import *
from accounts.models import Profile
from .forms import MessageForm, ChatForm
from django.http import HttpResponseNotFound
from django.db.models import Q


def new_chat(request):
    if request.method == 'POST':
        new_chat_form = ChatForm(request.POST)
        if new_chat_form.is_valid():
            new_chat_form.instance.creater = request.user
            #new_chat_form.instance.members =
            new_chat_form.save()
            return redirect('chat_url')
        else:
            HttpResponseNotFound("<h2>Введены неверные данные</h2>")
    else:
        new_chat_form = ChatForm()
    return render(request, 'chat/new_chat.html',
                  {'new_chat': new_chat_form})


#Перечисление всех чатов
def chat(request):
    search_chats = request.GET.get('search_chats', '')
    if search_chats:
        chats = Profile.objects.order_by('-pk').filter(Q(first_name__icontains=search_chats) | Q(last_name__icontains=search_chats))
    else:
        chats = Profile.objects.order_by('-pk')
    message_users = []
    #Перебираем все профили пользователя
    # for chat in chats:
        #Проверяем на наличие полученных\отправленных сообщений
        #Получаем последнее сообщение
    body_chat = Chat.objects.order_by('-pk').filter(Q(creater=request.user) | Q(members=request.user))

    for chat in body_chat:
        chat_id = get_object_or_404(Chat, slug=chat.slug)
        message = Message.objects.order_by('-pk').filter(Q(recipient=chat_id))[0:1]
        chat.message = message
    #last_message = Message.objects.filter('-pk')
        #Если есть сообщения - добавляем пользователя в список чатов
        # if body_chat:
        #     chat.message = body_chat
        #     message_users.append(chat)

    return render(request, 'chat/dialogs.html',
                  {'chat': body_chat,
                   #'last_message': body_message,
                   })
                   # 'body_chat': body_chat})


# Страница личного чата
def private_chat(request, slug):
    chat_id = get_object_or_404(Chat, slug=slug)
    body_chat = Message.objects.order_by('pk').filter(recipient=chat_id)
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message_form.instance.author = request.user
            message_form.instance.recipient = chat_id
            message_form.save()
            for_redirect = f"/chat/{chat_id}"
            return redirect(for_redirect)
        else:
            HttpResponseNotFound("<h2>Введены неверные данные</h2>")
    else:
        message_form = MessageForm()
    return render(request, 'chat/private_chat.html', {
                                                      'chat_id': chat_id,
                                                      'body_chat': body_chat,
                                                      'message_form': message_form,
                                                      })
