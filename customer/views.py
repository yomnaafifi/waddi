from rest_framework import status, generics
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from customer.models import Customer
from customer.serializer import BaseUserSerializer 

class CustomerSignupView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = BaseUserSerializer  

    # @extend_schema(responses= BaseUserSerializer)
    # def post(self, request, *args, **kwargs):
    #     if form.is_valid():
    #         user_data = form.save() #the saving logic is defined in the form itself 
    #         serializer = self.get_serializer(user_data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED) #should redirect to home? 
    #     else:
    #         return Response(form.errors, status=status.HTTP_400_BAD_REQUEST) 