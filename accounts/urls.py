from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login_url'),
    path('', views.out, name='out'),
    path('list_users/', views.list_users, name='list_users_url'),
    path('my_page/', views.my_page, name='my_page_url'),
    path('my_page/edit/', views.update_profile, name='my_page_edit_url'),
    path('my_page/edit_post/<int:id>/', views.update_post, name='edit_post_url'),
    path('my_page/delete_post/<int:id>/', views.delete_post, name='delete_post_url'),
    path('<str:slug>/', views.any_user, name='user_url'),
    #path('test/', views.any_user, name='user_url'),
]
