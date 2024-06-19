from rest_framework import serializers
from payment.models import Transactions


class CreateTXserializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        exclude = ["creation_date"]
