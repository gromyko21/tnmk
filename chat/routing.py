from django.urls import re_path
from .consumers import ChatConsumer, AllChatsConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
    re_path(r'^ws/user/(?P<user_id>[^/]+)/$', AllChatsConsumer),
    # re_path(r'^ws/chat/$', AllChatsConsumer),
]
