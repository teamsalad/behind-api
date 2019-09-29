from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chats.models import ChatMessage, ChatParticipant


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    ws/ --> Just for websocket stuff.
    path/ --> HTTP stuff.
    Use nginx and route both!

    I also need to find about how to write asynchronous consumers.
    https://channels.readthedocs.io/en/latest/topics/consumers.html
    I have to be careful on connecting Django models.

    `connect` and `disconnect` are websocket protocol layer functions.
    The other functions you define are events
    """
    async def connect(self):
        """
        Accept connection if user is authorized and
        is a participant of the chat room.
        :return: None
        """
        self.user = self.scope['user']
        self.chat_room_id = self.scope['url_route']['kwargs']['id']
        self.chat_room_group_name = f'chat_room_{self.chat_room_id}'
        if not self.user.is_authenticated:
            await self.disconnect(1000)
        elif not ChatParticipant.objects.filter(
                chat_room_id=self.chat_room_id,
                user_id=self.user.id
        ).exists():
            await self.disconnect(1001)
        else:
            await self.channel_layer.group_add(
                self.chat_room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, code):
        # TODO: use code to make error messages for disconnection reasons
        await self.channel_layer.group_discard(
            self.chat_room_group_name,
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        # Send message to room group
        if content['type'] == 'chat_message':
            await self.channel_layer.group_send(
                self.chat_room_group_name,
                {
                    'type': content['type'],
                    'message': content['message'],
                    'user_id': self.user.id
                }
            )
        if content['type'] == 'chat_timer':
            await self.channel_layer.group_send(
                self.chat_room_group_name,
                {
                    'type': content['type'],
                    'time_left': content['time_left'],
                    'user_id': self.user.id
                }
            )

    async def chat_message(self, event):
        message = event['message']
        # Save chat message
        if self.user.id == event['user_id']:
            await database_sync_to_async(ChatMessage.objects.create)(
                message=message,
                user_id=self.user.id,
                chat_room_id=self.chat_room_id
            )
        await self.send_json({
            'user_id': event['user_id'],
            'message': message
        })

    async def chat_timer(self, event):
        await self.send_json({
            'user_id': event['user_id'],
            'time_left': event['time_left']
        })
