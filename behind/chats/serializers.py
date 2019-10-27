import datetime

from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from rest_framework import serializers

from behind import settings, jarvis
from chats.models import (
    ChatRoom,
    ChatMessage,
    ChatParticipant,
    STATUS
)
from purchases.models import Purchase, STATE
from questions.models import Answer
from rewards.models import Gifticon
from users.models import User
from users.serializers import UserDetailsSerializer


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
            # Find and change the transaction to committed
            staging_purchase = Purchase.objects.filter(
                transaction_to_id=settings.TRANSACTION_STAGING_ACCOUNT_ID,
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
            # Send gifticon reward to answerer
            gifticon_type = ContentType.objects.get(
                app_label='rewards',
                model='gifticon'
            )
            unavailable_gifticon_ids = Purchase.objects.select_for_update() \
                .filter(item_type=gifticon_type) \
                .values_list('item_id', flat=True)
            available_gifticon = Gifticon.objects.select_for_update() \
                .exclude(id__in=unavailable_gifticon_ids) \
                .order_by('-expired_at') \
                .first()
            gifticon_left_count = Gifticon.objects.count() - len(unavailable_gifticon_ids)
            jarvis.send_slack(f"""
            기프티콘 남은 개수: {gifticon_left_count}
            """)
            if available_gifticon is None:
                raise serializers.ValidationError({
                    'gifticon': 'No gifticons left to reward.'
                })
            Purchase.objects.create(
                amount=available_gifticon.point_price,
                transaction_from_id=settings.TRANSACTION_STAGING_ACCOUNT_ID,
                transaction_to=instance.answer.answerer,
                item_id=instance.answer.id,
                item_type=answer_type,
                state=STATE[1][0]
            )
            Purchase.objects.create(
                amount=available_gifticon.point_price,
                transaction_from=instance.answer.answerer,
                transaction_to_id=settings.TRANSACTION_STAGING_ACCOUNT_ID,
                item_id=available_gifticon.id,
                item_type=gifticon_type,
                state=STATE[1][0]
            )
            # Change chat room status to stopped
            instance.state = validated_data['state']
            instance.save()
        return instance

    class Meta:
        model = ChatRoom
        fields = (
            'id', 'state', 'participants', 'messages',
            'answer', 'time_left', 'created_at',
        )
        read_only_fields = (
            'id', 'participants', 'messages',
            'answer', 'time_left', 'created_at',
        )
