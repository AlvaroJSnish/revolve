from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user_by_token(token):
    token_obj = Token.objects.get(key=token)
    user = token_obj.user
    return user
