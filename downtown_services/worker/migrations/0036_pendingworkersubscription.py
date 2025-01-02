# Generated by Django 5.1.1 on 2024-12-31 17:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0035_alter_workersubscription_stripe_price_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingWorkerSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_price_id', models.CharField(max_length=255, null=True)),
                ('stripe_product_id', models.CharField(max_length=255, null=True)),
                ('tier_name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('platform_fee_perc', models.IntegerField(default=1)),
                ('analytics', models.CharField(max_length=20)),
                ('service_add_limit', models.IntegerField(default=0)),
                ('service_update_limit', models.IntegerField(default=0)),
                ('user_requests_limit', models.IntegerField(default=0)),
                ('subscription_start_date', models.DateTimeField(blank=True, null=True)),
                ('subscription_end_date', models.DateTimeField(blank=True, null=True)),
                ('activation_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('worker_subscription', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pending_subscription', to='worker.workersubscription')),
            ],
        ),
    ]