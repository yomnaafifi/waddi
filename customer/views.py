from rest_framework import status, generics
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from customer.models import Customer
from customer.serializer import BaseUserSerializer, CustomerUserSerializer
from django.core.exceptions import ValidationError
from authentication.models import CustomUser
from datetime import date


VALID_USER = "valid user"
EXISTING_CREDINTALS = "user with either the email or usename already exist"


def validate_user_data(data):

    email = data["email"]

    if CustomUser.objects.filter(email=email).count() == 0:
        return VALID_USER
    else:
        return EXISTING_CREDINTALS


class CustomerSignupView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerUserSerializer

    @extend_schema(request=CustomerUserSerializer)
    def post(self, request, *args, **kwargs):
        print("testing:", request.data)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.create(**request.data["user"])
            customer = Customer.objects.create(user=user)
            customer.preferred_method = request.data["preferred_method"]
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )  # should redirect to home?
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # if form.is_valid():
    #     user_data = form.save() #the saving logic is defined in the form itself
    #     serializer = self.get_serializer(user_data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED) #should redirect to home?
    # else:
    #     return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
