from rest_framework.serializers import ModelSerializer
from driver.models import Driver

class CreateDriverSerializer(ModelSerializer):
    class Meta:
        model = Driver
        fields = ['email','first_name','last_name','birthdate','image','phone_no']