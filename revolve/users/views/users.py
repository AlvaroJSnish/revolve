from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from common.restrictions import check_projects_restrictions, check_database_restrictions, check_groups_restrictions
from common.serializers import GenericPaginationSerializer
from users.models.user import User
from users.serializers.user import UsersSerializer


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


class CheckUserProjects(ListAPIView):
    def get(self, request, *args, **kwargs):
        result_dict = {}

        user = authenticate(self.request)

        if user is None:
            result_dict['reasons'] = 'Please authenticate'
            result_status = status.HTTP_401_UNAUTHORIZED
            return Response(result_dict, result_status)
        else:
            available, slots, account_type = check_projects_restrictions(user)

            result_dict['available'] = available
            result_dict['slots'] = slots
            result_dict['account_type'] = account_type

            result_status = status.HTTP_200_OK

            return Response(result_dict, status=result_status)


class CheckUserDatabases(ListAPIView):
    def get(self, request, *args, **kwargs):
        result_dict = {}

        user = authenticate(self.request)

        if user is None:
            result_dict['reasons'] = 'Please authenticate'
            result_status = status.HTTP_401_UNAUTHORIZED
            return Response(result_dict, result_status)
        else:
            available, slots, account_type = check_database_restrictions(user)

            result_dict['available'] = available
            result_dict['slots'] = slots
            result_dict['account_type'] = account_type

            result_status = status.HTTP_200_OK

            return Response(result_dict, status=result_status)


class CheckUserGroups(ListAPIView):
    def get(self, request, *args, **kwargs):
        result_dict = {}

        user = authenticate(self.request)

        if user is None:
            result_dict['reasons'] = 'Please authenticate'
            result_status = status.HTTP_401_UNAUTHORIZED
            return Response(result_dict, result_status)
        else:
            available, slots, account_type = check_groups_restrictions(user)

            result_dict['available'] = available
            result_dict['slots'] = slots
            result_dict['account_type'] = account_type

            result_status = status.HTTP_200_OK

            return Response(result_dict, status=result_status)
