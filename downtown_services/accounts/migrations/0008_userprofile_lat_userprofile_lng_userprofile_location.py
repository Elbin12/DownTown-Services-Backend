# Generated by Django 5.1.1 on 2024-11-08 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_userprofile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='lat',
            field=models.DecimalField(decimal_places=20, default=1.2, max_digits=25),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lng',
            field=models.DecimalField(decimal_places=20, default=1.2, max_digits=25),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='location',
            field=models.CharField(default='Kochi', max_length=255),
        ),
    ]