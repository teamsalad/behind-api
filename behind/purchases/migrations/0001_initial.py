# Generated by Django 2.2.6 on 2019-10-04 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('item_id', models.PositiveIntegerField()),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'transaction'), (2, 'refund')], default=1)),
                ('state', models.PositiveSmallIntegerField(choices=[(1, 'staging'), (2, 'committed')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('transaction_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incomings', to=settings.AUTH_USER_MODEL)),
                ('transaction_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
