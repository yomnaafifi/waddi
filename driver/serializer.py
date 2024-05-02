from rest_framework.serializers import ModelSerializer
from driver.models import Driver
from authentication.models import CustomUser

class CreateDriverSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name','birthdate','image','phone_no']