# Generated by Django 5.0.4 on 2024-06-06 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0005_merge_0004_driver_city_0004_driver_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='car_license',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='driver_license',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
