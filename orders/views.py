from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from orders.models import Orders
from driver.models import Driver
from orders.serializers import (
    CreateOrderSerializer,
    CustomerHistorySerializer,
    DriverHistorySerializer,
    DriverInstanceSerializer,
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
    # queryset = Orders.objects.all()
    serializer_class = DriverHistorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = Orders.objects.filter(
            order_state="confirmed", customer_id=user.id
        ).order_by("-delivery_time")
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


# class TESTNEWSER(generics.ListAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = DriverUserSerializer


class ChangeOrderState(generics.UpdateAPIView):
    queryset = Orders.objects.all()
    serializer_class = CreateOrderSerializer

    def update(self, request, *args, **kwargs):
        order = Orders.object.get(order_id=id)
        new_state = request.data.get("new_state")
        if new_state in dict(Orders.STATE_CHOICES):
            order.order_state = new_state
            order.save()
            return Response(
                {"success": f"State changed to {new_state}"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid state"}, status=status.HTTP_400_BAD_REQUEST
            )
