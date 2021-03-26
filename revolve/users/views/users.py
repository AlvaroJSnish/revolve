from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from users.models.user import User
from users.serializers.user import UsersSerializer

from common.serializers import GenericPaginationSerializer


class UsersViewSet(ListAPIView):
    serializer_class = UsersSerializer
    pagination_class = GenericPaginationSerializer

    def get_queryset(self):
        result_status = status.HTTP_200_OK
        result_dict = {}

        filter_params = Q()

        user = authenticate(self.request)

        if user is not None:
            # result_status = status.HTTP_200_OK
            # result_dict["data"] = User.objects.filter(
            #     filter_params).distinct().exclude(is_deleted=True)
            return User.objects.filter(filter_params).distinct().exclude(is_deleted=True)
        else:
            # result_status = status.HTTP_400_BAD_REQUEST
            # result_dict["reasons"] = 'Credenciales inválidas'.format(
            #     user.email)
            return None
