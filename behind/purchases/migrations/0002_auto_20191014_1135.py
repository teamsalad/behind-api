# Generated by Django 2.2.6 on 2019-10-14 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('purchases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='transaction_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchase',
            name='transaction_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incomings', to=settings.AUTH_USER_MODEL),
        ),
    ]
