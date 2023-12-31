# Generated by Django 4.2.6 on 2023-11-03 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0009_productreview_purchase_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='crop_coordinates',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Crop Coordinates'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='cropped_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/cropped/', verbose_name='Cropped Image'),
        ),
    ]
