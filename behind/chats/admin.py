from django.contrib import admin

from chats.models import (
    ChatParticipant,
    ChatRoom,
    ChatMessage
)

admin.site.register(ChatParticipant)
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
