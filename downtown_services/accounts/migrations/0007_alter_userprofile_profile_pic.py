# Generated by Django 5.1.1 on 2024-10-24 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_userprofile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.FileField(blank=True, null=True, upload_to='users/profile_pic/'),
        ),
    ]
