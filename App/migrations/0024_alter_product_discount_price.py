# Generated by Django 4.2.6 on 2023-11-13 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0023_product_on_sale_alter_product_discount_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Discount Price'),
        ),
    ]
