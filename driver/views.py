from django.shortcuts import render
from rest_framework import generics, status
from drf_spectacular.utils import extend_schema
from driver.serializer import DriverUserSerializer
from rest_framework.response import Response
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
    serializer_class = CreateDriverUserSerializer

    # @extend_schema(responses=CreateDriverUserSerializer)
    # def post(self, request, *args, **kwargs):
    #     form = DriverSignupForm
    #     if form.is_valid():
    #         user_data = form.save()
    #         serializer = self.get_serializer(user_data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED) #should redirect to home? 
    #     else:
    #         return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
