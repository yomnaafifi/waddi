from rest_framework.serializers import ModelSerializer
from customer.models import Customer
from authentication.serializers import BaseUserSerializer
from django.utils.translation import gettext_lazy as _
import re
from django.contrib.auth import get_user_model

from authentication.models import CustomUser
from driver.models import Driver
from orders.models import Orders


class CustomerUserSerializer(ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Customer
        fields = ["user", "preferred_method"]


class DriverDetailsAsUserserializer(ModelSerializer):  # this is for onboarding api
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "image"]


class DriverDetailsAsDriver(ModelSerializer):
    user = DriverDetailsAsUserserializer()

    class Meta:
        model = Driver
        fields = ["user", "actual_car_license", "truck", "rating"]


class OnBoardingOrderserializer(ModelSerializer):
    driver = DriverDetailsAsDriver()

    class Meta:
        model = Orders
        fields = ["driver", "id", "order_state"]
