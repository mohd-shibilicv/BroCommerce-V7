# Generated by Django 4.2.6 on 2023-11-14 05:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0029_remove_category_discount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoryoffers',
            options={'verbose_name': 'Category Offer', 'verbose_name_plural': 'Category Offers'},
        ),
        migrations.AlterField(
            model_name='categoryoffers',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_offer', to='App.category'),
        ),
    ]