# Generated by Django 4.2.6 on 2023-11-08 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_delete_croppedimage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deliveryoptions',
            options={'ordering': ('order',), 'verbose_name': 'Delivery Option', 'verbose_name_plural': 'Delivery Options'},
        ),
    ]
