from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/local_chat$', consumers.ChatConsumer),
]