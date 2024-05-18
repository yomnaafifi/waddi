from django.shortcuts import render
from rest_framework import generics, status
from drf_spectacular.utils import extend_schema
from driver.serializer import DriverUserSerializer
from authentication.serializers import BaseUserSerializer, BaseUserDetails
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from driver.models import Driver
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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_data = request.data["user"]
            user_serializer = BaseUserSerializer(data=user_data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                user.is_driver = True
                user.save()
                driver = Driver.objects.create(user=user)
                driver.license = request.data["license"]
                driver.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriverDetailsView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = BaseUserDetails
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)
