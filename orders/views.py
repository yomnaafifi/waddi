from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from orders.models import Orders
from driver.models import Driver
from orders.serializers import (
    CreateOrderSerializer,
    CustomerHistorySerializer,
    DriverHistorySerializer,
    DriverUserSerializer,
)
from authentication.models import CustomUser
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class CreateOrderView(generics.CreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = CreateOrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                Driver.city, {"type": "order_message", "message": serializer.data}
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerShipmentHistoryView(generics.GenericAPIView):
    # queryset = Orders.models.filter(status="confirmed")
    serializer_class = CustomerHistorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = Orders.objects.filter(order_state="confirmed", customer_id=user.id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class DriverShipmentHistoryView(generics.GenericAPIView):
    serializer_class = DriverHistorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = Orders.objects.filter(order_state="confirmed", driver_id=user.id)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)


# class TESTNEWSER(generics.ListAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = DriverUserSerializer
