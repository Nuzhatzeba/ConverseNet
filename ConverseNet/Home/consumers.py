# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the user, thread, and friends involved in the conversation
        friend_name = self.scope['url_route']['kwargs']['friend_name']
        thread_id = self.scope['url_route']['kwargs']['thread_id']
        user_name = self.scope['url_route']['kwargs']['user_name']

        # Check if the user has permission to access this chat
        # You may want to add your own permission logic here

        # Create a chat group name for this conversation
        self.room_name = f"chat_{thread_id}"

        await self.channel_layer.group_add(self.room_name, self.channel_name)

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the WebSocket connection from the chat group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        message_data = json.loads(text_data)
        message = message_data['message']
        # Save the message to the database

        # Send the message to the chat group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat.message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({'message': message}))
