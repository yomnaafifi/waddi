from rest_framework.serializers import ModelSerializer
from customer.models import Customer
from authentication.models import CustomUser 

class BaseUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','password','first_name','last_name','birthdate','phone_no', 'age']


    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user