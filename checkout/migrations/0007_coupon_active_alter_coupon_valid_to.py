# Generated by Django 4.2.6 on 2023-11-09 07:46

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_remove_coupon_active_remove_coupon_discount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='valid_to',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 9, 7, 46, 36, 787908, tzinfo=datetime.timezone.utc)),
        ),
    ]