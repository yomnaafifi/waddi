from rest_framework import serializers
from orders.models import Orders


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


# make it return only those field sfor now
# its supposed to have: pickup&delivery locations, only show the delivery process of already delivered orders
