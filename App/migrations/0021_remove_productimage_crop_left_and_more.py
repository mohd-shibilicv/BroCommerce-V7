# Generated by Django 4.2.6 on 2023-11-11 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0020_productlanguage_product_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='crop_left',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='crop_lower',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='crop_right',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='crop_upper',
        ),
        migrations.AddField(
            model_name='productimage',
            name='cropped_data',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Cropped data'),
        ),
    ]