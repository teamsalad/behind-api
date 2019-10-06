from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from behind import settings
from purchases.models import Purchase
from purchases.models import ITEM_TYPE, ITEM_PRICE
from users.models import User


class CreatePurchaseSerializer(serializers.ModelSerializer):
    item_type = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=ContentType.objects.all(),
        write_only=True
    )
    item_id = serializers.IntegerField(
        required=True,
        write_only=True
    )

    @transaction.atomic
    def create(self, validated_data):
        if validated_data['item_type'].name == ITEM_TYPE[0]:
            validated_data['amount'] = ITEM_PRICE[ITEM_TYPE[0]]
        elif validated_data['item_type'].name == ITEM_TYPE[1]:
            # TODO: Implement payment flow
            pass
        else:
            raise serializers.ValidationError({
                'item_type': 'Invalid item type.'
            })
        validated_data['transaction_from'] = self.context['request'].user
        validated_data['transaction_to'] = User.objects.get(id=settings.TRANSACTION_STAGING_ACCOUNT_ID)
        return Purchase.objects.create(**validated_data)

    class Meta:
        model = Purchase
        fields = (
            'id', 'amount', 'item_type', 'item_id',
            'type', 'state', 'created_at',
        )
        read_only_fields = (
            'id', 'amount', 'type', 'state',
            'created_at',
        )


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = (
            'id', 'amount', 'item_type', 'item_id',
            'type', 'state', 'created_at',
        )
        read_only_fields = (
            'id', 'amount', 'type', 'state',
            'created_at',
        )
