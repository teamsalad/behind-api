from django.urls import path
from chats.views import (
    ChatRoomCreateView,
    ChatRoomDetailView,
)

urlpatterns = [
    path('', ChatRoomCreateView.as_view()),
    path('<int:id>/', ChatRoomDetailView.as_view()),
]
