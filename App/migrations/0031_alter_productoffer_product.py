# Generated by Django 4.2.6 on 2023-11-17 08:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0030_alter_categoryoffers_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoffer',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_offer', to='App.product'),
        ),
    ]
