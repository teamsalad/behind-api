from django.urls import path

from chats import consumers

websocket_urlpatterns = [
    path('ws/v1/chat_rooms/<int:id>/', consumers.ChatConsumer),
]