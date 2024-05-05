from django.db import models
from customer.models import Customer


class Orders(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_notes = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
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
    truck_types = {
        (1, "jumbo box 2700 kg"),
        (2, "jumbo box 5200 kg"),
        (3, "jumbo box 5200 kg"),
        (4, "tricycle 2700 kg"),
    }
    chosen_truck = models.CharField(max_length=100, choices=truck_types, null=True)
    pickup_time = models.DateTimeField()
    need_packing = models.BooleanField()
    need_labor = models.BooleanField()

    class Meta:
        db_table = "orders"
