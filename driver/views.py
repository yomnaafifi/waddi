from django.shortcuts import render
from rest_framework import generics, status
from drf_spectacular.utils import extend_schema
from driver.serializer import BaseUserSerializer, CreateDriverUserSerializer
from rest_framework.response import Response
from driver.models import Driver
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
