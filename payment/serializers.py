from rest_framework import serializers
from payment.models import Transactions


class CreateTXserializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        exclude = ["creation_date"]


class DriverTxHistory(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ["creation_date", "amount"]


class DriverEarnings(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ["amount"]
