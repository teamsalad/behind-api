from django.contrib import admin

from chats.models import (
    ChatParticipant,
    ChatRoom,
    ChatMessage
)


class ChatRoomAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class ChatParticipantAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class ChatMessageAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(ChatParticipant, ChatParticipantAdmin)
admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
