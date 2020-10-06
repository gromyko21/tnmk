from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Article
from django.db.models import Q
from .forms import *
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json


#Загрузка главной страницы
def home(request):
    #Поиск пользователей
    search_news = request.GET.get('search_news','')
    if search_news:
        article = Article.objects.filter(Q(title__icontains=search_news) | Q(text_article__icontains=search_news))
    else:
        article = Article.objects.order_by('-pk')

    #Пагинация новостей
    paginator = Paginator(article, 9)
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
    return render(request, 'home/home.html', data)


#Страница для каждой записи
def articles(request, slug):
    articles = get_object_or_404(Article, slug__iexact=slug)
    #Комментарии к записям
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.author = request.user
            comment_form.instance.post = articles
            comment_form.save()
            return redirect(articles)
    else:
        comment_form = CommentForm()

    comments = Comment.objects.order_by('-pk').filter(post=articles)
    context = {
        'articles':      articles,
        'comments':     comments,
        'comment_form': comment_form,
        'username': mark_safe(json.dumps(request.user.username)),
    }
    return render(request, 'home/one_news.html', context)


@login_required
def edit_comment(request, id, slug):
    try:
        articles = get_object_or_404(Article, slug__iexact=slug)
        comment_edit = Comment.objects.get(id=id)
        if request.method == "POST":
            comment_edit.body = request.POST.get("body")
            #post.image = request.POST.get('image')
            comment_edit.save()
            return redirect(articles)
        else:
            form = CommentForm()
            return render(request, "home/edit_comment.html",
                          {
                              "comment": comment_edit,
                           'username': mark_safe(json.dumps(request.user.username)),})
    except Comment.DoesNotExist:
        return HttpResponseNotFound("<h2>Post not found</h2>")


#Удаление комментариев
def delete_comment(request, id, slug):
    try:
        articles = get_object_or_404(Article, slug__iexact=slug)
        comment = Comment.objects.get(id=id)
        comment.delete()
        return redirect(articles)
    except Comment.DoesNotExist:
        return HttpResponseNotFound("<h2>Post not found</h2>")

