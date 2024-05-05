from rest_framework.serializers import ModelSerializer
from customer.models import Customer
from authentication.models import CustomUser
from django.utils.translation import gettext_lazy as _
import re
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class BaseUserSerializer(ModelSerializer):
    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            birthdate=validated_data["birthdate"],
            phone_no=validated_data["phone_no"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "birthdate",
            "phone_no",
        ]


class CustomerUserSerializer(ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Customer
        fields = ["user", "preferred_method"]
