from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_login, name='user_login_url'),
    path('', views.out, name='out'),
    path('my_page/', views.my_page, name='my_page_url'),
    path('my_page/edit/', views.update_profile, name='my_page_edit_url'),
    path('<str:slug>/', views.user, name='user_url'),
]
