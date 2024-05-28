# Generated by Django 5.0.4 on 2024-05-28 16:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_orders_commodity_image_orders_driver_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='chosen_truck',
            field=models.CharField(choices=[(2, 'jumbo box 5200 kg'), (4, 'tricycle 2700 kg'), (3, 'jumbo box 5200 kg'), (1, 'jumbo box 2700 kg')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_state',
            field=models.CharField(choices=[('assigned', 'Assigned'), ('delivered', 'Delivered'), ('unassigned', 'Unassigned'), ('confirmed', 'Confirmed'), ('pickup', 'Pickup')], default='unassigned', max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='time_created',
            field=models.TimeField(default=datetime.time(19, 54, 5, 749321)),
        ),
        migrations.AlterField(
            model_name='orders',
            name='type',
            field=models.CharField(choices=[('multiple commodities', 'Multiple Commodities '), ('wood', 'Wood'), ('appliances', 'Appliances'), ('glass', 'Glass'), ('food', 'Food'), ('plastic&rubber', 'Plastic and Rubber'), ('furniture', 'Furinture')], max_length=200),
        ),
    ]