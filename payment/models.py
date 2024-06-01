from django.db import models
from customer.models import Customer
from driver.models import Driver

payment_types = (
    ("withdraw", "Withdraw"),
    ("deposit", "Deposit"),
)
payment_methods = (
    (1, "Cash on Delivery"),
    (2, "Mobile Banking"),
    (3, "Credit or Debit Card"),
)


class Transactions(models.Model):
    payment_type = models.CharField(max_length=100, choices=payment_types)
    payment_method = models.CharField(max_length=100, choices=payment_methods)
    from_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="from_customer"
    )
    To_id = models.ForeignKey(
        Driver, on_delete=models.CASCADE, related_name="from_driver"
    )

    class Meta:
        db_table = "transactions"
