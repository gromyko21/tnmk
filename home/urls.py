from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home_url'),
    path('<str:slug>/', views.articles, name='articles_url'),
    path('edit_comment/<int:id>/', views.edit_comment, name='edit_comment_url'),
    path('delete_comment/<int:id>/', views.delete_comment, name='delete_comment_url'),
]
