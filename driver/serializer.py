from rest_framework.serializers import ModelSerializer
from driver.models import Driver
from authentication.serializers import BaseUserSerializer


class DriverUserSerializer(ModelSerializer):

    user = BaseUserSerializer()

    class Meta:
        model = Driver
        fields = ["user", "car_license", "driver_license"]


class AssignedDriverSerializer(ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Driver
        fields = [
            "user",
            "first_name",
            "last_name",
            "phone_no",
            "rating",
        ]  # should also return the order status,
