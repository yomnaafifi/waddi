# Generated by Django 5.0.4 on 2024-06-07 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_alter_orders_chosen_truck_alter_orders_order_state_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='chosen_truck',
            field=models.CharField(choices=[(1, 'small truck'), (4, 'tricycle'), (3, 'special large truck'), (2, 'large truck')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_state',
            field=models.CharField(choices=[('assigned', 'Assigned'), ('delivered', 'Delivered'), ('confirmed', 'Confirmed'), ('pickup', 'Pickup'), ('unassigned', 'Unassigned')], default='unassigned', max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='type',
            field=models.CharField(choices=[('furniture', 'Furinture'), ('multiple commodities', 'Multiple Commodities '), ('appliances', 'Appliances'), ('wood', 'Wood'), ('glass', 'Glass'), ('plastic&rubber', 'Plastic and Rubber'), ('food', 'Food')], max_length=200),
        ),
    ]
