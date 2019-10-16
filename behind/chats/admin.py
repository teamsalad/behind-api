from django.contrib import admin

from chats.models import (
    ChatParticipant,
    ChatRoom,
    ChatMessage
)


class ChatRoomAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('answer', 'time_left', 'state',)


class ChatParticipantAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('chat_room', 'user',)


class ChatMessageAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('chat_room', 'user', 'message',)


admin.site.register(ChatParticipant, ChatParticipantAdmin)
admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
