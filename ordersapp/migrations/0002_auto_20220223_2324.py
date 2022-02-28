# Generated by Django 3.1 on 2022-02-23 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordersapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('CREATED', 'CREATED'), ('IN PROCESSING', 'IN PROCESSING'), ('AWAITING_PAYMENT', 'AWAITING_PAYMENT'), ('PAID', 'PAID'), ('READY', 'READY'), ('CANCELLED', 'CANCELLED'), ('FINISHED', 'FINISHED')], default='CREATED', max_length=20, verbose_name="order's status"),
        ),
    ]
