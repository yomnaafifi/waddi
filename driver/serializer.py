from rest_framework.serializers import ModelSerializer
from driver.models import Driver
from authentication.models import CustomUser


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


class DriverUserSerializer(ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Driver
        fields = ["user", "license"]
