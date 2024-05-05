from rest_framework.serializers import ModelSerializer
from customer.models import Customer
from authentication.models import CustomUser 
from django.utils.translation import gettext_lazy as _
import re 


class BaseUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','password','first_name','last_name','birthdate','phone_no', 'age']


class CustomerUserSerializer(ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Customer
        fields = ['user', 'preferred_method']
    
    
