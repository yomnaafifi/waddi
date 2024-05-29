from django.db import models
from customer.models import Customer
from driver.models import Driver
from datetime import datetime


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = "location"


class Orders(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    dropoff_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    order_notes = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    time_created = models.TimeField(default=datetime.now().time())
    types = {
        ("plastic&rubber", "Plastic and Rubber"),
        ("appliances", "Appliances"),
        ("glass", "Glass"),
        ("wood", "Wood"),
        ("food", "Food"),
        ("furniture", "Furinture"),
        ("multiple commodities", "Multiple Commodities "),
    }
    type = models.CharField(max_length=200, choices=types)
    commodity_image = models.ImageField(upload_to=None, null=True)
    truck_types = {
        (1, "jumbo box 2700 kg"),
        (2, "jumbo box 5200 kg"),
        (3, "jumbo box 5200 kg"),
        (4, "tricycle 2700 kg"),
    }
    chosen_truck = models.CharField(max_length=100, choices=truck_types, null=True)
    pickup_date = models.DateField(null=True)
    pickup_time = models.TimeField(null=True)
    need_packing = models.BooleanField()
    need_labor = models.BooleanField()
    order_states = {
        ("unassigned", "Unassigned"),
        ("assigned", "Assigned"),
        ("pickup", "Pickup"),
        ("delivered", "Delivered"),
        ("confirmed", "Confirmed"),
    }
    order_state = models.CharField(
        max_length=100, choices=order_states, default="unassigned"
    )

    class Meta:
        db_table = "orders"
