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
    pickup_time = models.DateTimeField()
    need_packing = models.BooleanField()
    need_labor = models.BooleanField()

    class Meta:
        db_table = "orders"
