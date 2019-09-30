import datetime

from django.db import models

from behind import settings
from questions.models import Answer

STATUS = (
    (1, "STARTED"),
    (2, "STOPPED"),
)


class ChatRoom(models.Model):
    state = models.PositiveSmallIntegerField(
        choices=STATUS,
        default=STATUS[0][0]
    )
    answer = models.OneToOneField(
        Answer,
        on_delete=models.SET_NULL,
        null=True,
        related_name='chat_room'
    )
    time_left = models.TimeField(default=datetime.time(0, 20, 0))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'ChatRoom {self.id} {self.state}'

    class Meta:
        db_table = "chat_rooms"


class ChatParticipant(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='participating_chat_rooms'
    )
    chat_room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='participants'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'ChatParticipant {self.id}'

    class Meta:
        db_table = "chat_participants"


class ChatMessage(models.Model):
    message = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    chat_room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'ChatMessage {self.id} {self.message}'

    class Meta:
        db_table = "chat_messages"
