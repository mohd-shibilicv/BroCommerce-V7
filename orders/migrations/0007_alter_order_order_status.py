# Generated by Django 4.2.6 on 2023-10-28 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('paid', 'Paid'), ('pending', 'Pending'), ('cancelled', 'Cancelled')], default='pending', max_length=255),
        ),
    ]
