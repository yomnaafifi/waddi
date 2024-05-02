from django.db import models
from authentication.models import CustomUser

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    payment_methods = (
        (1, 'Cash on Delivery'),
        (2, 'Mobile Banking'),
        (3, 'Credit or Debit Card'), 
    )
    preferred_method = models.CharField(choices=payment_methods, max_length=50)