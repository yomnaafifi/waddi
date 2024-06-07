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

# Load the model and scaler


@api_view(["POST"])
def predict(request):

    try:
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

    except Exception as e:
        return JsonResponse(
            {"error": f"Failed to load model: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    try:
        # Load input data from request body
        if not request.body:
            return JsonResponse(
                {"error": "Request body is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        data = json.loads(request.body)
        # print(f"Received data: {data}")

        # Convert the input data into a DataFrame
        df = pd.DataFrame([data])
        # print(f"Input data as DataFrame:\n{df}")
        # Preprocess the data
        df["Truck"] = df["Truck"].str.replace("Large Truck ", "Large Truck")
        df["Truck"] = df["Truck"].str.replace("Small Truck ", "Small Truck")
        df["Truck"] = df["Truck"].str.replace("Medium Truck ", "Medium Truck")

        # Label encode the 'Truck' column if necessary
        # Make sure to use the same LabelEncoder that was used during training
        # label_encoder = joblib.load(
        #     "label_encoder.pkl"
        # )  # Assuming you saved the encoder as well
        df["Truck"] = label_encoder.transform(df["Truck"])

        # Perform one-hot encoding for categorical variables
        input_data_encoded = pd.get_dummies(df)
        # print(f"Encoded input data:\n{input_data_encoded}")

        # Ensure all expected columns are present
        expected_columns = set(["Truck", "weight", "Distance", "Add_Ons"])
        missing_cols = expected_columns - set(input_data_encoded.columns)
        for col in missing_cols:
            input_data_encoded[col] = 0

        # Reorder columns to match the training data
        input_data_encoded = input_data_encoded.reindex(
            columns=["Truck", "weight", "Distance", "Add_Ons"]
        )

        # Scale the input data
        input_data_scaled = scaler_X.transform(input_data_encoded)

        # Make a prediction
        prediction_scaled = rf_model_rus.predict(input_data_scaled)
        prediction = scaler_y.inverse_transform(
            prediction_scaled.reshape(-1, 1)
        ).flatten()

        return JsonResponse({"prediction": prediction.tolist()})

    except Exception as e:
        return JsonResponse(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class CreateOrderView(generics.GenericAPIView):
    queryset = Orders.objects.all()
    serializer_class = CreateShortOrderSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            # channel_layer = get_channel_layer()
            # async_to_sync(channel_layer.group_send)(
            #     Driver.city, {"type": "order_message", "message": serializer.data}
            # )
            try:
                order = Orders.objects.create(**serializer.validated_data)
                model_api_url = "http://127.0.0.1:8000/orders/predict/"
                response = requests.post(model_api_url, json=serializer.validated_data)

                if response.status_code == 200:
                    prediction = response.json().get("prediction")
                    if prediction:
                        order.pricing = prediction[0]
                        order.save()
                        return Response(
                            {"order_id": order.id, "predicted_price": prediction[0]},
                            status=status.HTTP_201_CREATED,
                        )
                    else:
                        return Response(
                            {"error": "Prediction response is invalid."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        )
                else:
                    return Response(
                        {"error": "Failed to get prediction from the model API"},
                        status=response.status_code,
                    )
            except requests.RequestException as e:
                return Response(
                    {"error": f"Request to model API failed: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            except Exception as e:
                return Response(
                    {"error": f"Failed to create order: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
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
