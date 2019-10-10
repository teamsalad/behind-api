from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from behind import settings

ITEM_TYPE = (
    'answer',
    'payment',
)
ITEM_PRICE = {
    'answer': 10000,
}
ITEM_COMMISSION = {
    'answer': 4000,
}
TYPE = (
    (1, 'transaction'),
    (2, 'refund'),
)
STATE = (
    (1, 'staging'),
    (2, 'committed'),
)


class Purchase(models.Model):
    amount = models.IntegerField()
    item_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    item_id = models.PositiveIntegerField()
    item = GenericForeignKey('item_type', 'item_id')
    transaction_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='outgoings'
    )
    transaction_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='incomings'
    )
    type = models.PositiveSmallIntegerField(
        choices=TYPE,
        default=TYPE[0][0]
    )
    state = models.PositiveSmallIntegerField(
        choices=STATE,
        default=STATE[0][0]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "purchases"
