# Generated by Django 5.0.4 on 2024-05-30 13:12

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_location_alter_orders_chosen_truck_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='dropoff_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dropoff', to='orders.location'),
        ),
        migrations.AddField(
            model_name='orders',
            name='pickup_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pickup', to='orders.location'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_state',
            field=models.CharField(choices=[('delivered', 'Delivered'), ('pickup', 'Pickup'), ('confirmed', 'Confirmed'), ('assigned', 'Assigned'), ('unassigned', 'Unassigned')], default='unassigned', max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='time_created',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='orders',
            name='type',
            field=models.CharField(choices=[('plastic&rubber', 'Plastic and Rubber'), ('appliances', 'Appliances'), ('wood', 'Wood'), ('furniture', 'Furinture'), ('glass', 'Glass'), ('food', 'Food'), ('multiple commodities', 'Multiple Commodities ')], max_length=200),
        ),
    ]
