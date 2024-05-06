from rest_framework.serializers import ModelSerializer
from customer.models import Customer
from authentication.serializers import BaseUserSerializer
from django.utils.translation import gettext_lazy as _
import re
from django.contrib.auth import get_user_model

from authentication.models import CustomUser


class CustomerUserSerializer(ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Customer
        fields = ["user", "preferred_method"]


class ListCustomersSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = ["image"]
