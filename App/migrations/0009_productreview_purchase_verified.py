# Generated by Django 4.2.6 on 2023-10-29 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_productreview_review_profile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='purchase_verified',
            field=models.BooleanField(default=False),
        ),
    ]
