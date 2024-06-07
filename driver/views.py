from django.shortcuts import render
from rest_framework import generics, status
from drf_spectacular.utils import extend_schema
from driver.serializer import DriverUserSerializer, AssignedDriverSerializer
from authentication.serializers import BaseUserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from driver.models import Driver
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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_data = request.data["user"]
            user_serializer = BaseUserSerializer(data=user_data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                user.is_driver = True
                user.save()
                driver = Driver.objects.create(user=user)
                driver.driver_license = request.data["driver_license"]
                driver.car_license = request.data["car_license"]
                driver.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
