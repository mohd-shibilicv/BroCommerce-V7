# Generated by Django 4.2.6 on 2023-11-02 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_croppedimage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CroppedImage',
        ),
    ]