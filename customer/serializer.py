from rest_framework.serializers import ModelSerializer
from customer.models import Customer
from authentication.models import CustomUser 

class CreateCustomerSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name','birthdate','image','phone_no']