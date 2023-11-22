# Generated by Django 4.2.6 on 2023-11-13 16:25

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0027_alter_product_discount_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='discount',
            field=models.IntegerField(default=0, editable=False, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Category Discount'),
        ),
        migrations.AddField(
            model_name='category',
            name='on_sale',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='CategoryOffers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('discount', models.IntegerField(default=0, help_text='In Percentage', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('is_active', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.category')),
            ],
        ),
    ]