from django.db import models
from customer.models import Customer
from driver.models import Driver
from datetime import datetime
from django.utils.timezone import now
from geopy.distance import geodesic


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    def distance_to(self, other_location):

        if other_location is None:
            return None

        # Create tuples of (latitude, longitude)
        point1 = (self.latitude, self.longitude)
        point2 = (other_location.latitude, other_location.longitude)

        # Calculate the distance
        distance = geodesic(point1, point2).kilometers

        return distance

    class Meta:
        db_table = "location"


types = {
    ("plastic&rubber", "Plastic and Rubber"),
    ("appliances", "Appliances"),
    ("glass", "Glass"),
    ("wood", "Wood"),
    ("food", "Food"),
    ("furniture", "Furinture"),
    ("multiple commodities", "Multiple Commodities "),
}

truck_types = {
    (1, "small truck"),
    (2, "large truck"),
    (3, "special large truck"),
    (4, "tricycle"),
}
order_states = {
    ("unassigned", "Unassigned"),
    ("assigned", "Assigned"),
    ("pickup", "Pickup"),
    ("delivered", "Delivered"),
    ("confirmed", "Confirmed"),
}


class Orders(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    pickup_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="pickup", null=True
    )
    dropoff_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="dropoff", null=True
    )
    order_notes = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    time_created = models.TimeField(default=now)
    type = models.CharField(max_length=200, choices=types)
    commodity_image = models.ImageField(upload_to="images/", null=True)
    chosen_truck = models.CharField(max_length=100, choices=truck_types, null=True)
    pickup_date = models.DateField(null=True)
    pickup_time = models.TimeField(null=True)
    delivery_date = models.DateField(null=True)
    delivery_time = models.TimeField(null=True)
    need_packing = models.BooleanField()
    need_labor = models.BooleanField()
    order_state = models.CharField(
        max_length=100, choices=order_states, default="unassigned"
    )
    pricing = models.IntegerField(null=True)

    @property
    def distance(self):

        if self.pickup_location and self.dropoff_location:
            return self.pickup_location.distance_to(self.dropoff_location)
        return None

    class Meta:
        db_table = "orders"
