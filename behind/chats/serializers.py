import datetime

from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from rest_framework import serializers

from behind import settings
from purchases.models import Purchase, STATE, ITEM_COMMISSION, ITEM_PRICE
from users.models import User
from users.serializers import UserDetailsSerializer
from questions.models import Answer
from chats.models import (
    ChatRoom,
    ChatMessage,
    ChatParticipant,
    STATUS
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
    time_left = serializers.TimeField(required=True)

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
            'id', 'participant_ids', 'answer_id', 'state', 'time_left',
            'participants', 'messages', 'created_at',
        )
        read_only_fields = (
            'id', 'state', 'participants', 'messages', 'created_at',
        )


class ChatRoomSerializer(serializers.ModelSerializer):
    participants = ChatParticipantSerializer(many=True, read_only=True)
    messages = ChatMessageSerializer(many=True, read_only=True)

    @transaction.atomic
    def update(self, instance, validated_data):
        if instance.time_left != datetime.time(0, 0, 0):
            raise serializers.ValidationError({
                'time_left': 'There should be no time left.'
            })
        if validated_data['state'] == STATUS[1][0]:
            answer_type = ContentType.objects.get(
                app_label='questions',
                model='answer'
            )
            transaction_staging_user = User.objects.get(
                id=settings.TRANSACTION_STAGING_ACCOUNT_ID
            )
            # Find and change the transaction to committed
            staging_purchase = Purchase.objects.filter(
                transaction_to=transaction_staging_user,
                item_id=instance.answer.id,
                item_type=answer_type,
                state=STATE[0][0]
            ).first()
            if staging_purchase is None:
                raise serializers.ValidationError({
                    'purchase': 'Already transacted points to answerer.'
                })
            staging_purchase.state = STATE[1][0]
            staging_purchase.save()
            # Send reward to the answerer
            Purchase.objects.create(
                amount=ITEM_PRICE[answer_type.name] - ITEM_COMMISSION[answer_type.name],
                transaction_from=transaction_staging_user,
                transaction_to=instance.answer.answerer,
                item_id=instance.answer.id,
                item_type=answer_type,
                state=STATE[1][0]
            )
            # Change chat room status to stopped
            instance.state = validated_data['state']
            instance.save()
        return instance

    class Meta:
        model = ChatRoom
        fields = (
            'id', 'state', 'participants', 'messages', 'time_left', 'created_at',
        )
        read_only_fields = (
            'id', 'participants', 'messages', 'time_left', 'created_at',
        )
