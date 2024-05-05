from rest_framework.serializers import ModelSerializer
from orders.models import Orders


class CreateOrderSerializer(ModelSerializer):
    model = Orders
    fields = "__all__"
