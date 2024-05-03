from django.db import models
from authentication.models import CustomUser

class Driver(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    license = models.CharField(max_length=255, null=False)
    is_online = models.BooleanField(default=False)
