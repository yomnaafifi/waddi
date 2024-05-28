import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from driver.models import driver


class DriverConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.driver_group_name = (
            "drivers"  # add city field to driver model and it should be the group name
        )

        await self.accept()

        await self.channel_layer.group_add(self.driver_group_name, self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.driver_group_name, self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        task_id = "12345"
        await self.channel_layer.group_send(
            self.driver_group_name,
            {
                "type": "task_id",
                "task_id": task_id,
            },
        )
