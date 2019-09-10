# Generated by Django 2.2.5 on 2019-09-10 07:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserJobHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmation_method', models.PositiveSmallIntegerField(choices=[(1, 'email'), (2, 'business_card'), (3, 'proof_of_employment')], default=1)),
                ('confirmed', models.BooleanField(default=False)),
                ('confirmation_information', models.TextField()),
                ('company', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='companies.Company')),
                ('job', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='companies.Job')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_job_histories',
            },
        ),
    ]