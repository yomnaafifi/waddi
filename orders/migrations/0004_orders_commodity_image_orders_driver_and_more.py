# Generated by Django 5.0.4 on 2024-05-27 19:27

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0003_remove_driver_license_driver_car_license_and_more'),
        ('orders', '0003_orders_pickup_date_orders_time_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='commodity_image',
            field=models.ImageField(null=True, upload_to=None),
        ),
        migrations.AddField(
            model_name='orders',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='driver.driver'),
        ),
        migrations.AddField(
            model_name='orders',
            name='order_state',
            field=models.CharField(choices=[('assigned', 'Assigned'), ('unassigned', 'Unassigned'), ('confirmed', 'Confirmed'), ('pickup', 'Pickup'), ('delivered', 'Delivered')], default='unassigned', max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='chosen_truck',
            field=models.CharField(choices=[(3, 'jumbo box 5200 kg'), (1, 'jumbo box 2700 kg'), (2, 'jumbo box 5200 kg'), (4, 'tricycle 2700 kg')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_notes',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='time_created',
            field=models.TimeField(default=datetime.time(22, 27, 54, 696817)),
        ),
        migrations.AlterField(
            model_name='orders',
            name='type',
            field=models.CharField(choices=[('wood', 'Wood'), ('food', 'Food'), ('appliances', 'Appliances'), ('glass', 'Glass'), ('multiple commodities', 'Multiple Commodities '), ('furniture', 'Furinture'), ('plastic&rubber', 'Plastic and Rubber')], max_length=200),
        ),
    ]