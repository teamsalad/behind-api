import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chats.models import ChatMessage, ChatParticipant, ChatRoom
from users.models import User


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    ws/ --> Just for websocket stuff.
    api/ --> HTTP stuff.
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
            await self.channel_layer.group_send(
                self.chat_room_group_name,
                {
                    'type': 'chat_state',
                    'user_id': self.user.id,
                    'state': 'CONNECTED'
                }
            )

    async def disconnect(self, code):
        # TODO: use code to make error messages for disconnection reasons
        await self.channel_layer.group_send(
            self.chat_room_group_name,
            {
                'type': 'chat_state',
                'user_id': self.user.id,
                'state': 'DISCONNECTED'
            }
        )
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
        if content['type'] == 'chat_state':
            await self.channel_layer.group_send(
                self.chat_room_group_name,
                {
                    'type': content['type'],
                    'state': content['state'],
                    'user_id': self.user.id
                }
            )

    async def chat_message(self, event):
        # Save chat message
        if self.user.id == event['user_id']:
            await database_sync_to_async(ChatMessage.objects.create)(
                message=event['message'],
                user_id=self.user.id,
                chat_room_id=self.chat_room_id
            )
            await self.send_push_notification(
                event['user_id'],
                event['message']
            )
        await self.send_json({
            'user_id': event['user_id'],
            'message': event['message']
        })

    async def chat_timer(self, event):
        hour, minute, second = (int(x) for x in event['time_left'].split(":"))
        chat_room = await self.update_time(
            self.chat_room_id,
            datetime.time(0, minute, second)
        )
        await self.send_json({
            'user_id': event['user_id'],
            'time_left': chat_room.time_left.strftime("%H:%M:%S")
        })

    @database_sync_to_async
    def update_time(self, chat_room_id, time_left):
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        if datetime.time(0, 0, 0) <= time_left < chat_room.time_left:
            chat_room.time_left = time_left
            chat_room.save()
        return chat_room

    @database_sync_to_async
    def send_push_notification(self, user_id, message):
        other_participant = ChatParticipant.objects \
            .filter(chat_room_id=self.chat_room_id) \
            .exclude(user_id=user_id) \
            .first()
        user = User.objects.get(id=other_participant.user_id)
        active_device = user.fcmdevice_set.filter(active=True).first()
        if active_device is not None:
            active_device.send_message(title=self.user.username, body=message)

    async def chat_state(self, event):
        await self.send_json({
            'user_id': event['user_id'],
            'state': event['state']
        })
