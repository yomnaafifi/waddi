import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from driver.models import Driver
from orders.models import Orders
from . import serializers


class DriverConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.driver_group_name = "tseting"
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

        await self.channel_layer.group_send(
            self.driver_group_name, {"type": "order_message", "message": message}
        )

    async def order_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))

    async def handle_accept_task(self, data):
        order_data = data("message")
        driver_id = self.scope["user"].id

        await self.save_order_data(order_data, driver_id)

        await self.send(  # this is notifying the driver
            text_data=json.dumps({"message": "Task accepted and assigned."})
        )

    @sync_to_async
    def save_order_data(self, order_data, driver_id):
        order = Orders.objects.create(
            id=order_data.get("id"),
            defaults={
                "driver_id": driver_id,
                "customer": order_data.get("customer"),
                "order_state": order_data.get(
                    "order_state"
                ),  # will test this data first then add the rest of it
            },
        )
