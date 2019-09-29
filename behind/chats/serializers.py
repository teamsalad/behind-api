from django.db import transaction
from rest_framework import serializers

from users.models import User
from users.serializers import UserDetailsSerializer
from questions.models import Answer
from chats.models import (
    ChatRoom,
    ChatMessage,
    ChatParticipant
)


class ChatParticipantSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()

    class Meta:
        model = ChatParticipant
        fields = (
            'id', 'user', 'created_at',
        )
        read_only_fields = (
            'id', 'user', 'created_at',
        )


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = (
            'id', 'message', 'user', 'created_at',
        )
        read_only_fields = (
            'id', 'user', 'created_at',
        )


class CreateChatRoomSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListField(
        required=True,
        write_only=True,
        child=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    )
    answer_id = serializers.PrimaryKeyRelatedField(
        required=True,
        write_only=True,
        queryset=Answer.objects.all()
    )
    participants = ChatParticipantSerializer(
        read_only=True,
        many=True
    )
    messages = ChatMessageSerializer(
        read_only=True,
        many=True
    )

    @transaction.atomic
    def create(self, validated_data):
        chat_room = ChatRoom.objects.create(answer=validated_data['answer_id'])
        participants = []
        for participant in validated_data['participant_ids']:
            participants.append(ChatParticipant.objects.create(
                user=participant,
                chat_room=chat_room
            ))
        return chat_room

    class Meta:
        model = ChatRoom
        fields = (
            'id', 'participant_ids', 'answer_id', 'state',
            'participants', 'messages', 'created_at',
        )
        read_only_fields = (
            'id', 'state', 'participants', 'messages', 'created_at',
        )


class ChatRoomSerializer(serializers.ModelSerializer):
    participants = ChatParticipantSerializer(many=True, read_only=True)
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = (
            'id', 'state', 'participants', 'messages', 'created_at',
        )
        read_only_fields = (
            'id', 'participants', 'messages', 'created_at',
        )
