# Generated by Django 5.1.1 on 2024-11-14 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0017_requests_is_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]