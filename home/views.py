from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Article
from django.db.models import Q
from .forms import *

def home(request):
    #Поиск пользователей
    search_news = request.GET.get('search_news','')
    if search_news:
        article = Article.objects.filter(Q(title__icontains=search_news) | Q(text_article__icontains=search_news))
    else:
        article = Article.objects.order_by('-pk')

    #Постраничная пагинация новостей
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
    }
    return render(request, 'home/home.html', data)

def articles(request, slug):
    articles = get_object_or_404(Article, slug__iexact=slug)
    #Комментарии

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            #form.instance.post = request.post_id
            form.save()
            return redirect("/")
        else:
            pass
            #messages.error(request, ('Пожалуйста, исправьте ошибки.'))
    else:
        form = CommentForm(instance=request.user)
    comment = Comment.objects.order_by('-pk')
    context = {
        'form':form,
        'comments': comment,
        'articles': articles,
    }
    return render(request, 'home/one_news.html', context)
