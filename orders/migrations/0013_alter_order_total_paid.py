# Generated by Django 4.2.6 on 2023-11-01 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_order_delivery_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_paid',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
