from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home_url'),
    path('<str:slug>/', views.articles, name='articles_url'),
]
