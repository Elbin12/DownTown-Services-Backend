# Generated by Django 5.1.1 on 2024-12-29 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0030_workerprofile_stripe_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='workerprofile',
            name='stripe_subscription_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='workerprofile',
            name='subscription_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
