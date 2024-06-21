from rest_framework import generics
from payment.models import Transactions
from payment.serializers import CreateTXserializer


class createtx(generics.CreateAPIView):
    queryset = Transactions.objects.all()
    serializer_class = CreateTXserializer
