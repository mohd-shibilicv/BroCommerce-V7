# Generated by Django 4.2.6 on 2023-11-21 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0033_alter_product_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='crop_left',
            field=models.FloatField(blank=True, default=0, help_text='Left coordinate', null=True),
        ),
        migrations.AddField(
            model_name='productimage',
            name='crop_lower',
            field=models.FloatField(blank=True, default=0, help_text='Lower coordinate', null=True),
        ),
        migrations.AddField(
            model_name='productimage',
            name='crop_right',
            field=models.FloatField(blank=True, default=0, help_text='Right coordinate', null=True),
        ),
        migrations.AddField(
            model_name='productimage',
            name='crop_upper',
            field=models.FloatField(blank=True, default=0, help_text='Upper coordinate', null=True),
        ),
    ]
