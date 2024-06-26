from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from customer.models import Customer
from authentication.serializers import BaseUserSerializer
from customer.serializer import (
    CustomerUserSerializer,
    OnBoardingOrderserializer,
)
from django.contrib.auth import get_user_model
from orders.models import Orders
from driver.models import Driver

VALID_USER = "valid user"
EXISTING_CREDINTALS = "user with either the email or usename already exist"

CustomUser = get_user_model()


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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_data = request.data["user"]
            user_serializer = BaseUserSerializer(data=user_data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                user.is_customer = True
                user.save()
                customer = Customer.objects.create(user=user)
                customer.preferred_method = request.data["preferred_method"]
                customer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OnBoardingOrderView(generics.GenericAPIView):
    serializer_class = OnBoardingOrderserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = Orders.objects.filter(customer_id=user.id).last()
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)
