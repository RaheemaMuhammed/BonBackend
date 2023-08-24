# consumers.py

import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer




class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        user = self.scope["user"]
        if not user.is_anonymous:
            # Add the user to the channel group
            await self.channel_layer.group_add(
                f"user_{user.id}", self.channel_name
            )

    async def disconnect(self, close_code):
        # Remove the user from the channel group on disconnect
        user = self.scope["user"]
        if not user.is_anonymous:
            await self.channel_layer.group_discard(
                f"user_{user.id}", self.channel_name
            )

    async def send_notification(self, event):
        notification = event["notification"]
        
        await self.send(text_data=json.dumps(notification))
