# Generated by Django 4.2.6 on 2023-11-03 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0015_remove_productimage_crop_coordinates_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='cropped_image',
        ),
    ]
