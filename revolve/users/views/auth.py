from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, authentication, status, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class SignInView(GenericAPIView):
    # authentication_classes = (PreUserTokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        result_status = status.HTTP_200_OK
        result_dict = {}

        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            result_status = status.HTTP_200_OK
            Token.objects.get_or_create(user=user)
            result_dict['user'] = {
                "id": user.id,
                "email": user.email,
            }
            result_dict['access_token'] = user.auth_token.key
        else:
            result_status = status.HTTP_400_BAD_REQUEST
            result_dict["reasons"] = 'Credenciales inválidas'

        return Response(result_dict, status=result_status)


class SignOutView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        result_status = status.HTTP_200_OK
        result_dict = {}
        logout(request)

        return Response(result_dict, status=result_status)
