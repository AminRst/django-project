from django.urls import re_path
from chat.consumers import ChatConsumer

# Room name is now part of the URL, e.g. ws://host/ws/chat/general/
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>[\w-]+)/$", ChatConsumer.as_asgi()),
]
