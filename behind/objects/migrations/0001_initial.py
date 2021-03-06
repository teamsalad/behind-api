# Generated by Django 2.2.6 on 2019-10-14 11:35

from django.db import migrations, models
import objects.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_alias', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'company'), (2, 'gifticon')])),
                ('state', models.PositiveSmallIntegerField(choices=[(1, 'staging'), (2, 'aliased'), (3, 'unaliased')], default=1)),
                ('object', models.FileField(upload_to=objects.models.storage_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'objects',
            },
        ),
    ]
