from django.db import models
from customer.models import Customer
from driver.models import Driver
from orders.models import Orders
from customer.models import Customer

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
    amount = models.FloatField(default=0.0)
    from_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="from_customer"
    )
    To_id = models.ForeignKey(
        Driver, on_delete=models.CASCADE, related_name="from_driver"
    )
    creation_date = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(
        Orders, on_delete=models.CASCADE, related_name="order_tx", null=True
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer_tx", null=True
    )
    driver = models.ForeignKey(
        Driver, on_delete=models.CASCADE, related_name="driver_tx", null=True
    )

    class Meta:
        db_table = "transactions"
