from rest_framework import generics, status
from orders.models import Orders
from orders.serializers import CreateOrderSerializer, ShipmentHistorySerializer
from rest_framework.response import Response


class CreateOrderView(generics.CreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = CreateOrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerShipmentHistoryView(generics.ListAPIView):
    serializer_class = ShipmentHistorySerializer

    def get_queryset(self):
        user_id = self.kwargs["pk"]  # Accessing the 'pk' parameter from URL
        return Orders.objects.filter(customer_id=user_id)
