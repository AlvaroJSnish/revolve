from rest_framework.authtoken.models import Token


def sync_user_by_token(token):
    token_obj = Token.objects.get(key=token)
    user = token_obj.user
    return user
