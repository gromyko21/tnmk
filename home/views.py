from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Article

def home(request):
    article = Article.objects.order_by('-pk')
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
        'prev_url': prev_url
    }
    return render(request, 'home/home.html', data)

def articles(request, slug):
    articles = get_object_or_404(Article, slug__iexact=slug)
    return render(request, 'home/one_news.html',
                  {'articles': articles})
