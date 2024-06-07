from rest_framework import serializers
from rest_framework.serializers import ValidationError
from orders.models import Orders
from driver.models import Driver
from authentication.models import CustomUser


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"


class CreateShortOrderSerializer(serializers.ModelSerializer):
    Distance = serializers.SerializerMethodField()
    Add_Ons = serializers.BooleanField(source="need_labor")
    Truck = serializers.CharField(source="chosen_truck")

    class Meta:
        model = Orders
        fields = ["Truck", "weight", "Distance", "Add_Ons"]


class CustomerHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = [
            "date_created",
            "time_created",
        ]


class DriverInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name"]  # + driver image

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.is_driver != True:
            raise ValidationError("The instance is not a driver.")
        return representation


class inbetweenSerializer(serializers.ModelSerializer):
    user = DriverInstanceSerializer()

    class Meta:
        model = Driver
        fields = ["user"]


class DriverHistorySerializer(serializers.ModelSerializer):
    driver = inbetweenSerializer()

    class Meta:
        model = Orders
        fields = ["driver", "pricing"]


# make it return only those field sfor now
# its supposed to have: pickup&delivery locations, only show the delivery process of already delivered orders
