from re import sub
from rest_framework.authtoken.models import Token
from django.contrib.auth.backends import BaseBackend


class TokenBackend(BaseBackend):
    def authenticate(self, request):
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        if header_token is not None:
            try:
                token = sub('Token ', '', request.META.get(
                    'HTTP_AUTHORIZATION', None))
                token_obj = Token.objects.get(key=token)
                request.user = token_obj.user
                return request.user
            except Token.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
