# Generated by Django 4.2.6 on 2023-10-28 04:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cod_payment',
        ),
    ]
