# Generated by Django 5.1.1 on 2024-11-13 04:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_orders'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_worker_arrived', models.BooleanField(default=False)),
                ('is_work_started', models.BooleanField(default=False)),
                ('arrival_time', models.DateTimeField(blank=True, null=True)),
                ('work_start_time', models.DateTimeField(blank=True, null=True)),
                ('work_end_time', models.DateTimeField(blank=True, null=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='status_tracking', to='accounts.orders')),
            ],
        ),
    ]
