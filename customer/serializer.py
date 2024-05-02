from rest_framework.serializers import ModelSerializer
from customer.models import Customer

class CreateCustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['email','first_name','last_name','birthdate','image','phone_no']