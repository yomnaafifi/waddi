from django.db import models
from authentication.models import CustomUser

class Driver(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)