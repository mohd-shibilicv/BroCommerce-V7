# Generated by Django 4.2.6 on 2023-11-21 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_customer_activation_link_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='activation_link_expiry',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
