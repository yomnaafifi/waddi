from django.db import models
from customer.models import Customer
from payment.models import Transactions
from datetime import datetime


class Orders(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
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
    transaction = models.ForeignKey(
        Transactions,
        on_delete=models.CASCADE,
        related_name="order_transaction",
        null=True,
        blank=True,
        default=None,
    )  # till we decide on suitable default

    class Meta:
        db_table = "orders"
