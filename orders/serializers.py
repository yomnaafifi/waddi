from rest_framework import serializers
from orders.models import Orders
from authentication.models import CustomUser


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"


class CustomerHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = [
            "date_created",
            "time_created",
        ]


class DriverUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name"]  # + driver image

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.is_driver != True:
            return None

        return representation


class DriverHistorySerializer(serializers.ModelSerializer):
    user = DriverUserSerializer()

    class Meta:
        model = Orders
        fields = ["user", "pricing"]


# make it return only those field sfor now
# its supposed to have: pickup&delivery locations, only show the delivery process of already delivered orders
