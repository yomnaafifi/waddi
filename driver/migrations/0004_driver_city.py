# Generated by Django 5.0.4 on 2024-05-28 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0003_remove_driver_license_driver_car_license_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='city',
            field=models.CharField(default='cairo', max_length=100),
        ),
    ]