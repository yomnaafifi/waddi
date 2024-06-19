import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from driver.models import Driver
from orders.models import Orders, Location
from orders.serializers import CreateOrderSerializer
from channels.db import database_sync_to_async
from typing import Any
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder


@database_sync_to_async
def create_order_db(order_data, user) -> dict[str, Any]:
    """create order from the data sent by the user"""
    kwargs = {}
    dropoff_location = Location.objects.create(
        latitude=order_data["dropoff_location"]["latitude"],
        longitude=order_data["dropoff_location"]["longitude"],
    )
    pickup_location = Location.objects.create(
        latitude=order_data["pickup_location"]["latitude"],
        longitude=order_data["pickup_location"]["longitude"],
    )
    kwargs["pickup_location"] = pickup_location
    kwargs["dropoff_location"] = dropoff_location
    if order_data.get("order_notes", None):
        kwargs["order_notes"] = order_data["order_notes"]
    if order_data.get("type", None):
        kwargs["type"] = order_data["type"]
    if order_data.get("chosen_truck", None):
        kwargs["chosen_truck"] = order_data["chosen_truck"]
    if order_data.get("pickup_date", None):
        kwargs["pickup_date"] = order_data["pickup_date"]
    if order_data.get("pickup_time", None):
        kwargs["pickup_time"] = order_data["pickup_time"]
    if order_data.get("need_packing", None):
        kwargs["need_packing"] = order_data["need_packing"]
    if order_data.get("need_labor", None):
        kwargs["need_labor"] = order_data.get("need_labor", None)
    if order_data.get("pricing", None):
        kwargs["pricing"] = order_data["pricing"]
    if order_data.get("weight", None):
        kwargs["weight"] = order_data["weight"]

    order = Orders.objects.create(customer=user, **kwargs)
    order.save()

    return model_to_dict(order)


@database_sync_to_async
def assign_order(order_id, user) -> dict[str, Any]:
    order = Orders.objects.get(id=order_id)
    order.driver = user
    order.order_state = "assigned"
    order.save(update_fields=["driver", "order_state"])


class DriverConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.driver_group_name = "tseting"
        self.user = self.scope["user"]

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

    ###############################################################
    ######################## ORDER  EVENTS ########################
    ###############################################################
    async def create_order(self, event):

        order_data = event["message"]
        # Validate the data using the serializer
        order = await create_order_db(order_data, self.user)
        await self.send(
            text_data=json.dumps(
                {
                    "type": "order_request",
                    "message": order,
                },
                cls=DjangoJSONEncoder,
            )
        )

    async def accept_order(self, event):
        order_id = event["message"]
        await assign_order(order_id, self.user)
        await self.send(
            text_data=json.dumps(
                {
                    "type": "clear_order",
                    "message": order_id,
                },
                cls=DjangoJSONEncoder,
            )
        )
