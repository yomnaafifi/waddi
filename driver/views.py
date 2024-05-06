from rest_framework import status, generics
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from driver.models import Driver
from driver.serializer import DriverUserSerializer
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth import get_user_model

VALID_USER = "valid user"
EXISTING_CREDINTALS = "user with either the email or usename already exist"

CustomUser = get_user_model()


def validate_user_data(data):

    email = data["email"]

    if CustomUser.objects.filter(email=email).count() == 0:
        return VALID_USER
    else:
        return EXISTING_CREDINTALS


class DriverSignupView(generics.CreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverUserSerializer

    @extend_schema(request=DriverUserSerializer)
    def post(self, request, *args, **kwargs):
        print("testing:", request.data)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.create(**request.data["user"])
            driver = Driver.objects.create(user=user)
            driver.preferred_method = request.data["license"]
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )  # should redirect to home?
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
