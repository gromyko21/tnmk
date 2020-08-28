from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.index, name='url_index'),
    re_path(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]
