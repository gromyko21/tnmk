from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django. contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator

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
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            #messages.success(request, ('Ваш профиль был успешно обновлен!'))
            return redirect('my_page_url')
        else:
            pass
            #messages.error(request, ('Пожалуйста, исправьте ошибки.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

#Загрузка личной страницы
def my_page(request):
    return render(request, 'accounts/my_page.html')

#Список всех пользователей
def list_users(request):
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
        'prev_url': prev_url
    }
    return render(request, 'accounts/list_users.html',data)

#Личные страницы пользователей
def user(request, slug):
    user = get_object_or_404(Profile, slug__iexact=slug)
    return render(request, 'accounts/profile_user.html',
                  {'user_data': user})



