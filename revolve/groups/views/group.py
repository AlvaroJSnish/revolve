from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response

from common.serializers import GenericPaginationSerializer
from groups.models import Group
from groups.serializers import GroupSerializer, GroupCreateSerializer, GroupsSerializer


class GroupsViewSet(ListCreateAPIView):
    pagination_class = GenericPaginationSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GroupCreateSerializer
        else:
            return GroupsSerializer

    def get_queryset(self):
        user = authenticate(self.request)

        if user is not None:
            return Group.objects.filter(Q(owner=user) | Q(users=user)).distinct().exclude(is_deleted=True)
        else:
            return None

    def post(self, request, *args, **kwargs):
        result_status = status.HTTP_201_CREATED
        result_dict = {}
        serializer = self.get_serializer(data=request.data)

        auth = authenticate(request)

        if auth:
            if not serializer.is_valid():
                result_status = status.HTTP_400_BAD_REQUEST
                result_dict["reasons"] = serializer.errors
            else:
                group = serializer.save()
                result_dict = GroupCreateSerializer(group).data
        else:
            result_status = status.HTTP_401_UNAUTHORIZED
            result_status["reasons"] = 'Not authorized'

        return Response(result_dict, status=result_status)


class GroupViewSet(RetrieveDestroyAPIView):
    serializer_class = GroupSerializer

    def get_object(self, queryset=None):
        auth = authenticate(self.request)

        if auth:
            return Group.objects.get(id=self.kwargs['group_id'])
        else:
            return None
