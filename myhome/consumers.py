import json
# from aioredis import Channel
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Channel
import logging
logger = logging.getLogger('consumer')

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "topic"
        self.room_group_name = "topic_group"

        # # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # Join mqtt group
        await self.channel_layer.group_add("mqttgroup", self.channel_name)
        # Ensure MQTT messages come to the room
        # This simplistic approach subscribes the room every
        # time a websocket connects but that's OK
        await self.channel_layer.send(
            "mqtt",
            {
                "type": "mqtt_subscribe",
                "topic": "topic",
                "group": "mqttgroup",
            },
        )
        await self.accept()
        logger.info("Connected to websocket")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        logger.info("Message received: {}".format(message))
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )
        # Publish on mqtt too
        await self.channel_layer.send(
            "mqtt",
            {
                "type": "mqtt_publish",
                "publish": {  # These form the kwargs for mqtt.publish
                    "topic": "topic_out",
                    "payload": message,
                    "qos": 2,
                    "retain": False,
                },
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        # await self.send(text_data=json.dumps({"message": message}))

    # Receive message from mqtt group and send to websocket
    async def mqtt_message(self, event):
        message = event["message"]
        topic = message["topic"]
        payload = message["payload"]

        logger.info("Received message from mqtt: {}".format(payload))

        chan = await database_sync_to_async(self.get_channel)()
        
        if payload == "ON" or payload == b'ON':
            chan.state = True
        else:
            chan.state = False
        
        await database_sync_to_async(chan.save)()

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": payload}))


    def get_channel(self):
        return Channel.objects.get(pk=3)