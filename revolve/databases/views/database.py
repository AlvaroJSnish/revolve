from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.response import Response

from common.serializers import GenericPaginationSerializer
from databases.classes import DatabaseConnector
from databases.models import Database
from databases.serializers import DatabaseSerializer


class DatabasesViewSet(ListCreateAPIView):
    serializer_class = DatabaseSerializer
    pagination_class = GenericPaginationSerializer

    def get_queryset(self):
        filter_params = Q()

        user = authenticate(self.request)

        if user is not None:
            return Database.objects.filter(filter_params, owner=user).distinct().exclude(is_deleted=True)
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
                database = serializer.save()
                result_dict = DatabaseSerializer(database).data
        else:
            result_status = status.HTTP_401_UNAUTHORIZED
            result_status["reasons"] = 'Not authorized'

        return Response(result_dict, status=result_status)


class DatabaseViewSet(CreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = DatabaseSerializer
    pagination_class = GenericPaginationSerializer

    def get_object(self, queryset=None):
        project = Database.objects.get(id=self.kwargs['project_id'])
        return project

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DatabaseConnect(CreateAPIView):
    def post(self, request, *args, **kwargs):
        result_status = status.HTTP_201_CREATED
        result_dict = {}

        auth = authenticate(request)

        if auth:
            database_name = request.data['database_name']
            database_host = request.data['database_host']
            database_port = request.data['database_port']
            database_password = request.data['database_password']
            database_type = request.data['database_type']
            database_user = request.data['database_user']

            database = DatabaseConnector(database_host=database_host, database_port=database_port,
                                         database_password=database_password, database_type=database_type,
                                         database_user=database_user, database_name=database_name)
            cursor = database.connect()

            if cursor is None:
                result_dict["reasons"] = 'Error: check credentials'
                result_status = status.HTTP_400_BAD_REQUEST
                return Response(result_dict, status=result_status)
            else:
                database.get_tables(cursor)

        else:
            result_status = status.HTTP_401_UNAUTHORIZED
            result_status["reasons"] = 'Not authorized'

        return Response(result_dict, status=result_status)
