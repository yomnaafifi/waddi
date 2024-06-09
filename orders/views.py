from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from orders.models import Orders
from driver.models import Driver
from orders.serializers import (
    CreateOrderSerializer,
    CreateShortOrderSerializer,
    CustomerHistorySerializer,
    DriverHistorySerializer,
    DriverInstanceSerializer,
)
from authentication.models import CustomUser
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from orders.pricingmodel import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.db import transaction
import pandas as pd
import joblib
import json
import requests


def predict(data):

    # try:
    rf_model_rus = joblib.load(
        "C:/Users/yomna/Desktop/waddi/orders/pricingmodel/model.pkl"
    )
    scaler_X = joblib.load(
        "C:/Users/yomna/Desktop/waddi/orders/pricingmodel/scaler_X.pkl"
    )
    scaler_y = joblib.load(
        "C:/Users/yomna/Desktop/waddi/orders/pricingmodel/scaler_Y.pkl"
    )
    label_encoder = joblib.load(
        "C:/Users/yomna/Desktop/waddi/orders/pricingmodel/label_encoder.pkl"
    )

    # except Exception as e:
    # return JsonResponse(
    #     {"error": f"Failed to load model: {str(e)}"},
    #     status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    # )

    # try:
    # if not request.body:
    #     return JsonResponse(
    #         {"error": "Request body is empty"}, status=status.HTTP_400_BAD_REQUEST
    # )

    # data = json.loads(request.body)
    # df = pd.DataFrame([data])

    # Check if the data is a list of dictionaries or a single dictionary
    if isinstance(data, dict):
        df = pd.DataFrame([data])  # Convert single dictionary to DataFrame
    elif isinstance(data, list):
        df = pd.DataFrame(data)  # Convert list of dictionaries to DataFrame
    df["Truck"] = df["Truck"].str.replace("Large Truck ", "Large Truck")
    df["Truck"] = df["Truck"].str.replace("Small Truck ", "Small Truck")
    df["Truck"] = df["Truck"].str.replace("Medium Truck ", "Medium Truck")
    df["Truck"] = label_encoder.transform(df["Truck"])

    input_data_encoded = pd.get_dummies(df)
    expected_columns = set(["Truck", "weight", "Distance", "Add_Ons"])
    missing_cols = expected_columns - set(input_data_encoded.columns)
    for col in missing_cols:
        input_data_encoded[col] = 0

    input_data_encoded = input_data_encoded.reindex(
        columns=["Truck", "weight", "Distance", "Add_Ons"]
    )
    input_data_scaled = scaler_X.transform(input_data_encoded)
    prediction_scaled = rf_model_rus.predict(input_data_scaled)
    prediction = scaler_y.inverse_transform(prediction_scaled.reshape(-1, 1)).flatten()
    pricing_int = prediction[0]
    return pricing_int
    # return JsonResponse({"prediction": prediction.tolist()})


# except Exception as e:
# return JsonResponse(
#     {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
# )


class testingshortserializer(generics.ListAPIView):
    queryset = Orders.objects.all()
    serializer_class = CreateShortOrderSerializer


class CalculatePriceView(generics.GenericAPIView):
    queryset = Orders.objects.all()
    serializer_class = CreateShortOrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            pricing = predict(request.data)
            validated_data = serializer.validated_data
            validated_data["pricing"] = pricing

            # serializer.save(pricing=pricing)
            # response_data = serializer.data
            # response_data["pricing"] = pricing
            return Response(pricing, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerShipmentHistoryView(generics.GenericAPIView):
    # queryset = Orders.models.filter(status="confirmed")
    serializer_class = CustomerHistorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = Orders.objects.filter(order_state="confirmed", customer_id=user.id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class DriverShipmentHistoryView(generics.GenericAPIView):
    # queryset = Orders.objects.all()
    serializer_class = DriverHistorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = Orders.objects.filter(
            order_state="confirmed", customer_id=user.id
        ).order_by("-delivery_time")
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


# class TESTNEWSER(generics.ListAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = DriverUserSerializer


class ChangeOrderState(generics.UpdateAPIView):
    queryset = Orders.objects.all()
    serializer_class = CreateOrderSerializer

    def update(self, request, *args, **kwargs):
        order = Orders.object.get(order_id=id)
        new_state = request.data.get("new_state")
        if new_state in dict(Orders.STATE_CHOICES):
            order.order_state = new_state
            order.save()
            return Response(
                {"success": f"State changed to {new_state}"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid state"}, status=status.HTTP_400_BAD_REQUEST
            )
