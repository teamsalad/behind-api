from django.db import models
from djmoney.models.fields import MoneyField
from django_mysql.models import JSONField

from behind import settings

AUTHORITY = (
    (1, 'behind'),
    (2, 'pg'),
)
STATUS = (
    (0, 'standby'),
    (1, 'committed'),
    (2, 'staging'),
    (3, 'committing'),
    (20, 'canceled'),
    (-20, 'cancel_failed'),
    (-30, 'canceling'),
    (-1, 'failed'),
    (-2, 'commit_failed'),
)


class Payment(models.Model):
    """
    Information about price max digits and decimal places.
    https://stackoverflow.com/questions/224462/storing-money-in-a-decimal-column-what-precision-and-scale/224866#224866
    """
    receipt_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    item_name = models.CharField(max_length=150)
    price = MoneyField(
        max_digits=19,
        decimal_places=4,
        default_currency='KRW'
    )
    pg_alias = models.CharField(max_length=100)
    method_alias = models.CharField(max_length=20)
    pg_name = models.CharField(max_length=100)
    method_name = models.CharField(max_length=100)
    pg_response = JSONField()
    requested_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField()
    status = models.SmallIntegerField(choices=STATUS, default=STATUS[0][0])
    authority = models.SmallIntegerField(choices=AUTHORITY, default=AUTHORITY[1][0])
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payments"
