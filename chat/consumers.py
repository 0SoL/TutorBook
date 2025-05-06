import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync


User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket CONNECTING")
        try:
            self.room_id = self.scope['url_route']['kwargs']['room_id']
            self.room_group_name = f'chat_{self.room_id}'

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            print("WebSocket CONNECTED SUCCESSFULLY")

        except Exception as e:
            print("WebSocket CONNECT ERROR:", str(e))
    
    async def disconnect(self, close_code):
        # При отключении — покидаем группу
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = self.scope['user'].id  # Кто отправил сообщение

        await self.save_message(sender_id, self.room_id, message)

        # Отправляем сообщение обратно всем в группе
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
            }
        )
        
    async def chat_message(self, event):
        # Когда приходит сообщение из группы — отправляем его клиенту
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
        }))
        
    @database_sync_to_async
    def save_message(self, sender_id, room_id, message):
        # Функция для сохранения сообщения в БД
        sender = User.objects.get(id=sender_id)
        room = ChatRoom.objects.get(id=room_id)
        Message.objects.create(chatroom=room, sender=sender, text=message)