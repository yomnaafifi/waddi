from rest_framework import generics, status
from rest_framework.response import Response
from payment.models import Transactions
from payment.serializers import CreateTXserializer, DriverTxHistory, DriverEarnings
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated


def get_filter_date(self, period):
    now = datetime.now()
    if period == "Day":
        start_date = now - timedelta(days=1)
    elif period == "Week":
        start_date = now - timedelta(weeks=1)
    elif period == "All Time":
        start_date = datetime.min
    else:
        raise ValueError("Invalid period specified")
    return start_date


class createtx(generics.CreateAPIView):
    queryset = Transactions.objects.all()
    serializer_class = CreateTXserializer


class drivertxhistory(generics.GenericAPIView):
    serializer_class = DriverTxHistory
    permission_classes = [IsAuthenticated]

    def get(
        self,
        request,
        period,
    ):
        user = request.user
        date = get_filter_date(period)
        transactions = Transactions.objects.filter(
            driver_id=user.id, creation_date=date
        )  # queryset
        serializer = self.serializer_class(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class driverearnings(generics.GenericAPIView):
    serializer_class = DriverEarnings
    permission_classes = [IsAuthenticated]

    def get(
        self,
        request,
        period,
    ):
        user = request.user
        date = get_filter_date(period)
        transactions = Transactions.objects.filter(
            driver_id=user.id, creation_date=date
        )  # queryset
        total_earnings = sum(tx.amount for tx in transactions)
        return Response({"total_earnings": total_earnings}, status=status.HTTP_200_OK)
