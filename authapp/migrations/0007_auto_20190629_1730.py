# Generated by Django 2.2.2 on 2019-06-29 17:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_auto_20190629_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expire',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 1, 17, 30, 48, 912096, tzinfo=utc)),
        ),
    ]
