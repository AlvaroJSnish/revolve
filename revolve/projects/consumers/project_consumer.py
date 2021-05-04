import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ProjectConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def connect(self):
        self.user_token = self.scope['url_route']['kwargs']['user_id']
        # self.user = await get_user_by_token(self.user_token)
        # self.projects = await get_user_projects(self.user)
        self.room = self.user_token

        await self.channel_layer.group_add(
            self.room,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room,
            self.channel_name
        )
        await self.close(close_code)

    # from websocket
    # async def receive(self, text_data):
    #     print("RECEIVE")
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #
    #     await self.channel_layer.group_send(
    #         self.room,
    #         {
    #             'type': 'updated_project',
    #             'message': message
    #         }
    #     )

    async def updated_project(self, event):
        await self.send(text_data=json.dumps({
            'type': 'updated_project',
            'message': event['message']
        }))
