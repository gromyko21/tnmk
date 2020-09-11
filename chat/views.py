from django.shortcuts import render, redirect, reverse, get_list_or_404, get_object_or_404
from .models import *
from accounts.models import Profile
from .forms import MessageForm
from django.http import HttpResponseNotFound
from django.db.models import Q


#Перечисление всех чатов
def chat(request):
    chats = Profile.objects.order_by('-pk')
    message_users = []
    #Перебираем все профили пользователя
    for chat in chats:
        #Проверяем на наличие полученных\отправленных сообщений
        #Получаем последнее сообщение
        body_chat = Message.objects.order_by('-pk').filter(Q(author=request.user, recipient=chat.user) |
                                                      Q(author=chat.user, recipient=request.user))[0:1]
        #Если есть сообщения - добавляем пользователя в список чатов
        if body_chat:
            chat.message = body_chat
            message_users.append(chat)

    return render(request, 'chat/dialogs.html',
                  {'chat': message_users,})
                   #'body_chat': body_chat})


#Страница личного чата
def private_chat(request, slug):
    user_profile = get_object_or_404(Profile, slug__iexact=slug)
    body_chat = Message.objects.order_by('pk').filter(Q(author=request.user, recipient=user_profile.user) |
                                                      Q(author=user_profile.user, recipient=request.user))

    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message_form.instance.author = request.user
            message_form.instance.recipient = user_profile.user
            message_form.save()
            for_redirect = '/chat/{}'.format(user_profile.slug)
            return redirect(for_redirect)
        else:
            HttpResponseNotFound("<h2>Введены неверные данные</h2>")
    else:
        message_form = MessageForm()
    return render(request, 'chat/private_chat.html', {
                                                      'body_chat': body_chat,
                                                      'message_form': message_form,
                                                      })
