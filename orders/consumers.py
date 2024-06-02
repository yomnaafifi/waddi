import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from driver.models import Driver
from orders.models import Orders
from orders.serializers import CreateOrderSerializer


class DriverConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.driver_group_name = "tseting"
        self.user = self.scope["user"]
        self.user_id = self.user.id
        # self.driver_city
        # should use sth like scope but not sure yet
        # add city field to driver model and it should be the group name
        # how do i only add the drivers to the correct group based on the city

        await self.accept()

        await self.channel_layer.group_add(self.driver_group_name, self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.driver_group_name, self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        type_ = data["type"]

        await self.channel_layer.group_send(
            self.driver_group_name, {"type": type_, "message": message}
        )

    async def order_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))

    async def handle_accept_task(self, data):
        # here the driver will accept the task and the data will be sent to the server
        # here the driver should send the id of the order he accepted
        # and the server should update the order state to assigned with the driver to be the id of the user
        # and then send id of the accepted order so that the front should remove it from all the drivers subscribed to the socket in the app UI
        # the message will be the id of the order and the status to order-assigned
        # so no other driver can send a another request to the same order from the UI
        order_data = data("message")
        driver_id = self.scope["user"].id

        await self.save_order_data(order_data)

        await self.send(  # this is notifying the driver
            text_data=json.dumps({"message": "Task accepted and assigned."})
        )

    @sync_to_async
    def save_order_data(self, order_data):
        # here you should create the order object from the data the user will send
        # then save it to the database
        # the schema of data the user will return
        # the data will be :
        # {
        #     customer_id,
        #     order_state:"default is unassigned",
        #     pickup_location: {latitude, longitude},
        #     dropoff_location: {latitude, longitude},
        #     order_notes,
        #     type(types): (plastic&rubber, appliances, glass, wood, food, furniture, multiple commodities),
        #     commodity_image:optional,
        #     chosen_truck,:(range from 1 to 4),
        #     pickup_date,
        #     pickup_time,
        #     need_packing,
        #     need_labor,
        #     order_state:(unassigned, assigned, pickup, delivered, confirmed)

        # }

        # Validate the data using the serializer
        serializer = CreateOrderSerializer(
            data=order_data
        )  # i dont get which format should get into the serialzier
        if serializer.is_valid():
            validated_data = serializer.validated_data
            order = Orders.objects.create(
                id=validated_data["id"],
                customer_id=validated_data["customer_id"],
                driver_id=validated_data["user_id"],
                pickup_location=validated_data["pickup_location"],
                dropoff_location=validated_data["dropoff_location"],
                order_notes=validated_data["order_notes"],
                type=validated_data["type"],
                commodity_image=validated_data["commodit_image"],
                chosen_truck=validated_data["chosen_truck"],
                pickup_date=validated_data["pickup_date"],
                pickup_time=validated_data["pickup_time"],
                need_packing=validated_data["need_packing"],
                need_labour=validated_data["need_labour"],
                order_state=validated_data["order_state"],
            )
        return order.data
        # will test this data first then add the rest of it

        ############################################################

        # then u create the data and validarate it with a serializer and save it
        # order = serializer.data
        # then u publish to all subscribers the order data "not all fields just the required" and the type of message will be order_request
