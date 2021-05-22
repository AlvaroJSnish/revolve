from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response

from common.serializers import GenericPaginationSerializer
from databases.classes import DatabaseConnector
from databases.models import Database
from databases.serializers import DatabaseSerializer, DatabasesSerializer
from projects.models import Project
from projects.serializers import ProjectSerializer


class DatabasesViewSet(ListCreateAPIView):
    serializer_class = DatabasesSerializer
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
            # available = check_database_restrictions(auth)

            # if available:
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
        user = authenticate(self.request)

        if user:
            database = Database.objects.get(id=self.kwargs['database_id'])
            return database
        else:
            return None

    def destroy(self, request, *args, **kwargs):
        user = authenticate(self.request)

        if user:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return None


class CheckDbConnection(CreateAPIView):
    def post(self, request, *args, **kwargs):
        result_status = status.HTTP_200_OK
        result_dict = {}

        auth = authenticate(request)

        if auth:
            db_values = get_database_values(request.data)
            database = create_database(db_values)
            cursor = database.connect()

            if cursor is not None:
                result_dict['message'] = 'databases.connectedSuccessfully'
                result_dict['status'] = 1
                database.disconnect()

            else:
                result_status = status.HTTP_400_BAD_REQUEST
                result_dict['message'] = 'databases.connectedError'
                result_dict['status'] = 0

        else:
            result_status = status.HTTP_401_UNAUTHORIZED
            result_status["reasons"] = 'Not authorized'

        return Response(result_dict, status=result_status)


class DatabaseTables(ListAPIView):
    def get(self, request, *args, **kwargs):
        result_status = status.HTTP_201_CREATED
        result_dict = {}

        auth = authenticate(request)

        if auth:
            database = Database.objects.get(id=self.kwargs['database_id'])
            connection = DatabaseConnector(
                database_host=database.database_host,
                database_type=database.database_type,
                database_name=database.database_name,
                database_user=database.database_user,
                database_port=database.database_port,
                database_password=database.database_password
            )
            cursor = connection.connect()

            if cursor is None:
                result_status = status.HTTP_400_BAD_REQUEST
                result_dict["reasons"] = 'databases.connectedError'

                return Response(result_dict, status=result_status)
            else:
                tables = connection.get_tables()

                table_names = [table[0] for table in tables]

                result_dict['tables'] = table_names
                connection.disconnect()

        else:
            result_status = status.HTTP_401_UNAUTHORIZED
            result_status["reasons"] = 'Not authorized'

        return Response(result_dict, status=result_status)


class DatabaseGetTable(ListAPIView):
    def get(self, request, *args, **kwargs):
        result_status = status.HTTP_201_CREATED
        result_dict = {}

        auth = authenticate(request)

        if auth:
            database = Database.objects.get(id=self.kwargs['database_id'])
            connection = DatabaseConnector(
                database_host=database.database_host,
                database_type=database.database_type,
                database_name=database.database_name,
                database_user=database.database_user,
                database_port=database.database_port,
                database_password=database.database_password
            )
            cursor = connection.connect()

            if cursor is None:
                result_status = status.HTTP_400_BAD_REQUEST
                result_dict["reasons"] = 'databases.connectedError'

                return Response(result_dict, status=result_status)
            else:
                rows = connection.get_table(table_name=self.kwargs['table_name'], with_headers=True)

                filtered_projects = Project.objects.filter(owner=auth)
                projects_config_from_db = [project for project in filtered_projects if
                                           project.project_configuration.created_from_database and project.project_name ==
                                           self.kwargs['table_name']]

                if len(projects_config_from_db):
                    result_dict['project'] = ProjectSerializer(projects_config_from_db[0]).data
                    result_dict['has_project'] = True
                else:
                    result_dict['project'] = None
                    result_dict['has_project'] = False

                result_dict['rows'] = rows
                connection.disconnect()

        else:
            result_status = status.HTTP_401_UNAUTHORIZED
            result_status["reasons"] = 'Not authorized'

        return Response(result_dict, status=result_status)


def get_database_values(data):
    database_name = data['database_name']
    database_host = data['database_host']
    database_port = data['database_port']
    database_password = data['database_password']
    database_type = data['database_type']
    database_user = data['database_user']

    return {'database_user': database_user, 'database_host': database_host, 'database_port': database_port,
            'database_password': database_password, 'database_type': database_type, 'database_name': database_name}


def create_database(db_values):
    db_connector = DatabaseConnector(database_host=db_values['database_host'],
                                     database_port=db_values['database_port'],
                                     database_type=db_values['database_type'],
                                     database_user=db_values['database_user'],
                                     database_name=db_values['database_name'],
                                     database_password=db_values['database_password'])

    return db_connector
