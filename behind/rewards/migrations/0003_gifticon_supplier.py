# Generated by Django 2.2.6 on 2019-10-13 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rewards', '0002_auto_20191013_0350'),
    ]

    operations = [
        migrations.AddField(
            model_name='gifticon',
            name='supplier',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
