import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
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
    def connect(self):
        """
        Accept connection if user is authorized and
        is a participant of the chat room.
        :return: None
        """
        self.user = self.scope['user']
        self.chat_room_id = self.scope['url_route']['kwargs']['id']
        self.chat_room_group_name = f'chat_room_{self.chat_room_id}'
        # TODO: use code to make error messages for disconnection reasons
        if not self.user.is_authenticated:
            self.disconnect(1000)
        # TODO: Validate if chat room exists and user is participant
        async_to_sync(self.channel_layer.group_add)(
            self.chat_room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        # Send message to room group
        if text_data_json['type'] == 'chat_message':
            async_to_sync(self.channel_layer.group_send)(
                self.chat_room_group_name,
                {
                    'type': text_data_json['type'],
                    'message': text_data_json['message']
                }
            )
        if text_data_json['type'] == 'chat_timer':
            async_to_sync(self.channel_layer.group_send)(
                self.chat_room_group_name,
                {
                    'type': text_data_json['type'],
                    'time_left': text_data_json['time_left']
                }
            )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'user_id': self.user.id,
            'message': event['message']
        }))

    def chat_timer(self, event):
        self.send(text_data=json.dumps({
            'user_id': self.user.id,
            'time_left': event['time_left']
        }))
