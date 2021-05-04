import json

from channels.generic.websocket import AsyncWebsocketConsumer

from common.serializers import UUIDEncoder
from projects.serializers import ProjectSerializer
from websockets import get_user_by_token, get_user_projects


class ProjectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_token = self.scope['url_route']['kwargs']['user_id']
        self.user = await get_user_by_token(self.user_token)
        self.projects = await get_user_projects(self.user)

        self.room = str(self.user.id)

        await self.channel_layer.group_add(self.room, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room, self.channel_name)
        await self.close(close_code)

    # from websocket
    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room,
            {
                'type': 'get_projects',
                'message': 'hi'
            }
        )

    # from room group
    async def get_projects(self, event):
        await self.send(text_data=json.dumps({
            'key': 'get_user_projects',
            'data': [ProjectSerializer(project).data for project in self.projects]
        }, cls=UUIDEncoder))
