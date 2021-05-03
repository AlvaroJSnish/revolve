from channels.generic.websocket import AsyncWebsocketConsumer


class ProjectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_token = self.scope['url_route']['kwargs']['user_id']
        
        await self.accept()
        pass

    async def disconnect(self, close_code):
        pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        pass
