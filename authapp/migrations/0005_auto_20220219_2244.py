# Generated by Django 3.1 on 2022-02-19 17:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_auto_20220219_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 21, 17, 44, 49, 618797, tzinfo=utc)),
        ),
    ]
