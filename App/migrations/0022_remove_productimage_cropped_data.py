# Generated by Django 4.2.6 on 2023-11-11 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0021_remove_productimage_crop_left_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='cropped_data',
        ),
    ]