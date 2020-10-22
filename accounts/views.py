from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from .forms import *
from .models import *
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from chat.models import Chat, Message
from chat.forms import ChatForm
from django.db.models import Count
from django.utils.safestring import mark_safe
import json


#Авторизация пользователей
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home_url')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/auth.html', {'form': form})


#Выход из ЛК пользователя
def out(request):
    logout(request)
    return redirect('home_url')


#Создание и обновление данных профиля
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('my_page_url')
        else:
            pass
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit.html', {
        'profile_form': profile_form,
        'username': mark_safe(json.dumps(request.user.username)),
    })


#Загрузка личной страницы
def my_page(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect("my_page_url")
        else:
            pass
    else:
        form = PostForm()

    context = {
            'posts': Post.objects.all(),
            'my_posts': Post.objects.filter(author=request.user),
            'form': form,
            'username': mark_safe(json.dumps(request.user.username)),
        }
    return render(request, 'accounts/my_page.html', context)


#Обновить данные поста
@login_required
def update_post(request, id):
    try:
        post = Post.objects.get(pk=id)
        if request.method == "POST":
            post_form = PostForm(request.POST, request.FILES, instance=post)
            post.text = request.POST.get("text")
            post.image = request.POST.get('image')
            post_form.save()
            post.save()
            return redirect("my_page_url")
        else:
            post_form = PostForm(instance=post)
            return render(request, "accounts/edit_post.html",
                          {
                              "post": post,
                              'post_form': post_form,
                              'username': mark_safe(json.dumps(request.user.username)),
                           })
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Post not found</h2>")


def delete_post(request, id):
    try:
        person = Post.objects.get(id=id)
        person.delete()
        return redirect("my_page_url")
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Post not found</h2>")


#Список всех пользователей
def list_users(request):
    #Поиск пользователей
    search_users = request.GET.get('search_name', '')
    if search_users:
        list_users = Profile.objects.filter(Q(first_name__icontains=search_users) | Q(last_name__icontains=search_users))
    else:
        list_users = Profile.objects.order_by('-pk')

    paginator = Paginator(list_users, 15)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    data = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
        'username': mark_safe(json.dumps(request.user.username)),
    }
    return render(request, 'accounts/list_users.html',data)


# Личные страницы пользователей
def any_user(request, slug):
    # Получение данных профиля конкретного пользователя
    any_user = get_object_or_404(Profile, slug=slug)
    # Новости на личной странице пользователя
    user_context = Post.objects.filter(author=any_user.user)
    if request.method == 'POST':
        new_chat_form = ChatForm(request.POST)
        chat_prov = Chat.objects.filter((Q(creater=request.user) & Q(members=any_user.user.id)) |
                                        (Q(creater=any_user.user.id) & Q(members=request.user)))
        # Ищем личный чат между 2 пользователями
        if chat_prov:
            for i in chat_prov:
                # Если хоть один личный чат существует - не создаем комнату
                if i.members.count() == 2:
                    count = 2
                    if count == 2:
                        return redirect('chat_url')
            else:
                if new_chat_form.is_valid():
                    new_chat_form.instance.creater = request.user
                    new_chat_form.save()

                    return redirect('chat_url')
                else:
                    HttpResponseNotFound("<h2>Введены неверные данные</h2>")
        else:
            if new_chat_form.is_valid():
                new_chat_form.instance.creater = request.user
                new_chat_form.save()
                return redirect('chat_url')
            else:
                HttpResponseNotFound("<h2>Введены неверные данные</h2>")
    else:
        new_chat_form = ChatForm()
    context = {
             'user_data': any_user,
             'user_context': user_context,
             'start_chat': new_chat_form,
             'username': mark_safe(json.dumps(request.user.username)),
                }
    return render(request, 'accounts/profile_user.html', context)
