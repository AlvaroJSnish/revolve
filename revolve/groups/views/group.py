from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, CreateAPIView
from rest_framework.response import Response

from common.serializers import GenericPaginationSerializer
from databases.models import Database
from groups.models import Group
from groups.serializers import GroupSerializer, GroupCreateSerializer, GroupsSerializer
from projects.models import Project


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


class GroupAddDatabase(CreateAPIView):
    def post(self, request, *args, **kwargs):
        result_status = status.HTTP_201_CREATED
        result_dict = {}

        auth = authenticate(request)

        if auth:
            database_id = self.kwargs["database_id"]
            database = Database.objects.get(id=database_id, owner_id=auth.id)

            if database:
                group_id = self.kwargs["group_id"]
                group = Group.objects.get(id=group_id)

                group.databases.add(database)
                group.save(force_update=True)

                result_status = status.HTTP_201_CREATED
                result_dict["group"] = GroupSerializer(group).data

            else:
                result_status = status.HTTP_400_BAD_REQUEST
                result_dict["reasons"] = 'Not authorized to add this database'

        else:
            result_status = status.HTTP_401_UNAUTHORIZED
            result_status["reasons"] = 'Not authorized'

        return Response(result_dict, status=result_status)


class GroupAddProject(CreateAPIView):
    def post(self, request, *args, **kwargs):
        result_status = status.HTTP_201_CREATED
        result_dict = {}

        auth = authenticate(request)

        if auth:
            project_id = self.kwargs["project_id"]
            project = Project.objects.get(id=project_id, owner_id=auth.id)

            if project:
                group_id = self.kwargs["group_id"]
                group = Group.objects.get(id=group_id)

                group.projects.add(project)
                group.save(force_update=True)

                result_status = status.HTTP_201_CREATED
                result_dict["group"] = GroupSerializer(group).data

            else:
                result_status = status.HTTP_400_BAD_REQUEST
                result_dict["reasons"] = 'Not authorized to add this project'

        else:
            result_status = status.HTTP_401_UNAUTHORIZED
            result_status["reasons"] = 'Not authorized'

        return Response(result_dict, status=result_status)


class GroupAddUser(CreateAPIView):
    def post(self, request, *args, **kwargs):
        result_status = status.HTTP_201_CREATED
        result_dict = {}

        auth = authenticate(request)

        if auth:
            invitation_code = self.kwargs['invitation_code']

            if invitation_code:
                group = Group.objects.get(invitation_code=invitation_code)

                group.users.add(auth)
                group.save(force_update=True)

                result_status = status.HTTP_201_CREATED
                result_dict["group"] = GroupSerializer(group).data
            else:
                result_status = status.HTTP_400_BAD_REQUEST
                result_dict["reason"] = "You need to pass an invitation code"

        else:
            result_status = status.HTTP_401_UNAUTHORIZED
            result_status["reasons"] = 'Not authorized'

        return Response(result_dict, status=result_status)
