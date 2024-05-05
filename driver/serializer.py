from rest_framework.serializers import ModelSerializer
from driver.models import Driver
from authentication.serializers import BaseUserSerializer


class CreateDriverUserSerializer(ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Driver
        fields = ['user', 'license']