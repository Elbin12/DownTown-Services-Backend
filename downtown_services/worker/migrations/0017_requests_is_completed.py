# Generated by Django 5.1.1 on 2024-11-12 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0016_alter_workerprofile_lat_alter_workerprofile_lng_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requests',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]