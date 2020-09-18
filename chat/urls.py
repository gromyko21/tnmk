from django.urls import path
from . import views


urlpatterns = [
     path('', views.chat, name='chat_url'),
     path('new_chat/', views.new_chat, name='new_chat_url'),
     path('<str:id>/', views.private_chat, name='private_chat_url'),
    # path('', views.dialogs, name='dialogs'),
    # path('create/<user_id>/', views.CreateDialogView, name='create_dialog'),
    # path('<chat_id>/', views.MessagesView.as_view(), name='messages'),
]
