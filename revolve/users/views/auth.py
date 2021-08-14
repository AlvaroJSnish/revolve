import json
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from users.serializers import UserCreateSerializer
from users.tasks import disabled_trial_account
from userstats.models import UserStats


class SignInView(GenericAPIView):
    # authentication_classes = (PreUserTokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        result_status = status.HTTP_200_OK
        result_dict = {}

        # body = json.loads(request.body.decode('utf-8'))
        email = request.data['email']
        password = request.data['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            result_status = status.HTTP_200_OK
            Token.objects.get_or_create(user=user)
            result_dict['user'] = {
                "id": user.id,
                "email": user.email,
                "avatar": user.avatar,
                "username": user.username,
                "account_type": user.account_type,
                "disabled": user.disabled
            }
            result_dict['access_token'] = user.auth_token.key

        else:
            result_status = status.HTTP_400_BAD_REQUEST
            result_dict["reasons"] = 'Credenciales inválidas'

        return Response(result_dict, status=result_status)


class SignUpView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        result_status = status.HTTP_201_CREATED
        result_dict = {}
        email = request.data['email']
        password = make_password(request.data['password'])
        data = {
            'email': email,
            'password': password
        }

        serializer = self.get_serializer(data=data)

        if not serializer.is_valid():
            result_status = status.HTTP_400_BAD_REQUEST
            result_dict["reasons"] = serializer.errors
        else:
            user_serialized = serializer.save()
            user = authenticate(
                request, email=user_serialized.email, password=request.data['password'])
            login(request, user)
            result_status = status.HTTP_200_OK
            Token.objects.get_or_create(user=user)

            # user stats
            UserStats.objects.create(user=user)

            result_dict['user'] = {
                "id": user.id,
                "email": user.email,
                "avatar": user.avatar,
                "username": user.username,
                "account_type": user.account_type,
                "disabled": user.disabled
            }
            result_dict['access_token'] = user.auth_token.key

            two_weeks = datetime.utcnow() + timedelta(days=14)
            disabled_trial_account.apply_async(args=[user.id], eta=two_weeks)

        return Response(result_dict, status=result_status)


class SignOutView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        result_status = status.HTTP_200_OK
        result_dict = {}
        logout(request)

        return Response(result_dict, status=result_status)
