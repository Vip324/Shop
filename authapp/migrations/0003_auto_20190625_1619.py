# Generated by Django 2.2.2 on 2019-06-25 16:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_auto_20190623_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expire',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 27, 16, 19, 27, 701742, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
