# Generated by Django 5.1.1 on 2024-11-08 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0015_workerprofile_lat_workerprofile_lng_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workerprofile',
            name='lat',
            field=models.DecimalField(decimal_places=20, max_digits=25),
        ),
        migrations.AlterField(
            model_name='workerprofile',
            name='lng',
            field=models.DecimalField(decimal_places=20, max_digits=25),
        ),
        migrations.AlterField(
            model_name='workerprofile',
            name='location',
            field=models.CharField(max_length=255),
        ),
    ]
