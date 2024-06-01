import random
from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


def generate_random_rating():
    return round(random.uniform(1.0, 5.0), 1)


class Driver(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    car_license = models.ImageField(upload_to=None, null=True)  # further edits needed
    driver_license = models.ImageField(
        upload_to=None, null=True
    )  # further edits needed
    is_online = models.BooleanField(default=False)
    rating = models.FloatField(default=generate_random_rating)
