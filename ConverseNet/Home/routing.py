# routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<friend_name>\w+)/(?P<thread_id>\d+)/(?P<user_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
