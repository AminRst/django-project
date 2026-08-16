import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Room name now comes from the WebSocket URL (see chat/routing.py)
        # instead of being hardcoded, so multiple independent chat rooms
        # can run at once.
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.roomGroupName = f"chat_{self.room_name}"
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Bugfix: this used to pass self.channel_layer (the layer object)
        # instead of self.channel_name (this connection's channel id) as the
        # second argument, which raised an error whenever a client
        # disconnected.
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
            })

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({"message": message, "username": username}))
