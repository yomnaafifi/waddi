import random
from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


def generate_random_rating():
    return round(random.uniform(1.0, 5.0), 1)


truck_types = [
    "Ford F-150",
    "Chevrolet Silverado",
    "Ram 1500",
    "Toyota Tundra",
    "GMC Sierra",
    "Nissan Titan",
    "Honda Ridgeline",
    "Jeep Gladiator",
    "Ford Ranger",
    "Chevrolet Colorado",
]

truck_type = random.choice(truck_types)


def generate_random_license():
    numbers = [str(random.randint(1, 9)) for _ in range(3)]
    arabic_letters = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
    letters = [random.choice(arabic_letters) for _ in range(3)]
    result = "".join(numbers) + " " + "".join(letters)
    return result


class Driver(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    car_license = models.ImageField(
        upload_to="images/", null=True
    )  # will remove null when we enter data
    city = models.CharField(max_length=100, default="cairo")
    driver_license = models.ImageField(upload_to="images/", null=True)
    is_online = models.BooleanField(default=False)
    rating = models.FloatField(default=generate_random_rating)
    truck = models.CharField(max_length=100, default=truck_type)
    actual_car_license = models.CharField(
        max_length=100, default=generate_random_license
    )
