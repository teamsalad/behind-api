from django.db import models
from djmoney.models.fields import MoneyField


class Gifticon(models.Model):
    name = models.CharField(max_length=100)
    exchange = models.CharField(max_length=100)
    point_price = models.IntegerField()
    price = MoneyField(
        max_digits=19,
        decimal_places=4,
        default_currency='KRW'
    )
    barcode_number = models.CharField(max_length=100)
    expired_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
