from django.urls import path
from . import views


urlpatterns = [
     path('messages/', views.all_message),
     path('', views.chat, name='chat_url'),
     path('new_chat/', views.new_chat, name='new_chat_url'),
     path('upload/', views.upload_private_chat, name='upload'),
     path('<str:id>/', views.private_chat, name='private_chat_url'),
     path('delete_message/<int:id>/', views.delete_message, name='delete_message_url'),
     path('edit_chat/<int:id>/', views.update_chat, name='edit_chat_url'),
]
