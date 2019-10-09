from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from behind import settings
from purchases.models import Purchase, STATE
from purchases.models import ITEM_TYPE, ITEM_PRICE


class CreatePurchaseSerializer(serializers.ModelSerializer):
    item_type = serializers.ChoiceField(
        choices=ITEM_TYPE,
        write_only=True
    )
    item_id = serializers.IntegerField(
        required=True,
        write_only=True
    )

    @transaction.atomic
    def create(self, validated_data):
        if validated_data['item_type'] == ITEM_TYPE[0]:
            if self.context['request'].user.balance() - ITEM_PRICE[ITEM_TYPE[0]] < 0:
                raise serializers.ValidationError({
                    'balance': 'Not enough points.'
                })
            validated_data['item_type'] = ContentType.objects.get(
                app_label='questions',
                model='answer'
            )
            if Purchase.objects.filter(
                    item_type=validated_data['item_type'],
                    item_id=validated_data['item_id'],
                    transaction_to_id=settings.TRANSACTION_STAGING_ACCOUNT_ID,
                    state=STATE[0][0]
            ).exists():
                raise serializers.ValidationError({
                    'purchase': 'Already paid for chatting with answerer.'
                })
            validated_data['amount'] = ITEM_PRICE[ITEM_TYPE[0]]
        elif validated_data['item_type'] == ITEM_TYPE[1]:
            # TODO: Implement payment flow
            pass
        else:
            raise serializers.ValidationError({
                'item_type': 'Invalid item type.'
            })
        validated_data['transaction_from'] = self.context['request'].user
        validated_data['transaction_to_id'] = settings.TRANSACTION_STAGING_ACCOUNT_ID
        return Purchase.objects.create(**validated_data)

    class Meta:
        model = Purchase
        fields = (
            'id', 'amount', 'item_type', 'item_id',
            'transaction_from', 'transaction_to',
            'type', 'state', 'created_at',
        )
        read_only_fields = (
            'id', 'amount', 'type', 'state',
            'transaction_from', 'transaction_to',
            'created_at',
        )


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = (
            'id', 'amount', 'item_type', 'item_id',
            'transaction_from', 'transaction_to',
            'type', 'state', 'created_at',
        )
        read_only_fields = (
            'id', 'amount', 'type', 'state',
            'transaction_from', 'transaction_to',
            'created_at',
        )
