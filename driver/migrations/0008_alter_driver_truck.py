# Generated by Django 5.0.4 on 2024-06-08 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0007_driver_actual_car_license_driver_truck'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='truck',
            field=models.CharField(default='Chevrolet Colorado', max_length=100),
        ),
    ]