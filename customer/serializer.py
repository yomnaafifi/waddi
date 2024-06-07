from rest_framework.serializers import ModelSerializer
from customer.models import Customer
from authentication.serializers import BaseUserSerializer
from django.utils.translation import gettext_lazy as _
import re
from django.contrib.auth import get_user_model

from authentication.models import CustomUser
from driver.models import Driver


class CustomerUserSerializer(ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Customer
        fields = ["user", "preferred_method"]


class OnBoardingOrderSerializer(ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Driver
        fields = [
            "user",
            "first_name",
            "last_name",
            "phone_no",
            "rating",
        ]
