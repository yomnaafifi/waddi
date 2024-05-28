import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync


class DriverConsumer(WebsocketConsumer):
    def connect(self):
        self.driver_group_name = (
            "drivers"  # add city field to driver model and it should be the group name
        )

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.driver_group_name, self.channel_name
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.driver_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        task_id = "12345"
        async_to_sync(self.channel_layer.group_send)(
            self.driver_group_name,
            {
                "type": "task_id",
                "task_id": task_id,
            },
        )
