from django.db import models


class Gifticon(models.Model):
    name = models.CharField(max_length=100)
    exchange = models.CharField(max_length=100)
    barcode_number = models.CharField(max_length=100)
    expired_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
