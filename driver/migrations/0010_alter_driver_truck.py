# Generated by Django 5.0.4 on 2024-06-19 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0009_alter_driver_truck'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='truck',
            field=models.CharField(default='Chevrolet Colorado', max_length=100),
        ),
    ]
