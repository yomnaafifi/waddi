# Generated by Django 5.0.4 on 2024-06-19 15:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
        ('driver', '0010_alter_driver_truck'),
        ('orders', '0018_remove_orders_transaction_alter_orders_chosen_truck_and_more'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='amount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='transactions',
            name='creation_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='transactions',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_tx', to='customer.customer'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver_tx', to='driver.driver'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_tx', to='orders.orders'),
        ),
    ]