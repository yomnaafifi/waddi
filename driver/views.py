from django.shortcuts import render
from rest_framework import generics, status
from driver.serializer import CreateDriverSerializer
from authentication.forms import DriverSignupForm
from rest_framework.response import Response
class DriverSignupView(generics.CreateAPIView):
    serializer_class = CreateDriverSerializer
    def post(self, request, *args, **kwargs):
        form = DriverSignupForm
        if form.is_valid():
            user_data = form.save()
            serializer = self.get_serializer(user_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED) #should redirect to home? 
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
