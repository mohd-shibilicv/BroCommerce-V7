# Generated by Django 4.2.6 on 2023-11-15 12:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_referral_customer_referral_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='referral',
            old_name='created_at',
            new_name='created',
        ),
        migrations.RemoveField(
            model_name='referral',
            name='referred_code',
        ),
        migrations.RemoveField(
            model_name='referral',
            name='referrer_code',
        ),
        migrations.AddField(
            model_name='customer',
            name='referral_link',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='referral',
            name='referred_customer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referred_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='referral',
            name='referring_customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referrals', to=settings.AUTH_USER_MODEL),
        ),
    ]
