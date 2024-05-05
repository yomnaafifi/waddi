from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class Driver(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    license = models.CharField(max_length=255, null=True)
    is_online = models.BooleanField(default=False)
