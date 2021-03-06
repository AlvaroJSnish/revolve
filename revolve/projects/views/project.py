import csv
import io
import shutil
from re import sub
from uuid import uuid4

import joblib
import numpy as np
import pandas as pd
from django.contrib.auth import authenticate
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from common.restrictions import check_projects_restrictions
from common.serializers import GenericPaginationSerializer
from projects.models import Project, ProjectConfiguration, ProjectConfigFile
from projects.serializers import ProjectSerializer, ProjectConfigurationSerializer, ProjectFilesSerializer, \
    ProjectLiteSerializer
from projects.tasks import train_regression_model
from userstats.models import ProjectVisits

UPLOAD_DIR = '../../uploads/'


class ProjectsViewSet(ListCreateAPIView):
    serializer_class = ProjectSerializer
    pagination_class = GenericPaginationSerializer

    def get_queryset(self):
        filter_params = Q()

        user = authenticate(self.request)

        if user:
            return Project.objects.filter(filter_params, owner=user).distinct().exclude(is_deleted=True)
        else:
            return None

    def post(self, request, *args, **kwargs):
        auth = authenticate(request)
        result_status = status.HTTP_201_CREATED
        result_dict = {}

        if auth:
            serializer = self.get_serializer(data=request.data)

            available = check_projects_restrictions(auth)

            if available:
                if not serializer.is_valid():
                    result_status = status.HTTP_400_BAD_REQUEST
                    result_dict["reasons"] = serializer.errors
                else:
                    project = serializer.save()

                    # initialize project visits
                    ProjectVisits.objects.create(project=project)

                    result_dict = ProjectSerializer(project).data
            else:
                result_status = status.HTTP_400_BAD_REQUEST
                result_dict["reasons"] = "User can't create more projects"
                result_dict["api_error_code"] = 101
        else:
            result_status = status.HTTP_401_UNAUTHORIZED
            result_status["reasons"] = 'Not authorized'

        return Response(result_dict, status=result_status)


class ProjectsLite(ListAPIView):
    serializer_class = ProjectLiteSerializer

    def get_queryset(self):
        filter_params = Q()

        user = authenticate(self.request)

        if user:
            return Project.objects.filter(filter_params, owner=user).distinct().exclude(is_deleted=True)
        else:
            return None


class ProjectViewSet(CreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    pagination_class = GenericPaginationSerializer

    def get_object(self, queryset=None):
        auth = authenticate(self.request)

        if auth:
            project = Project.objects.get(id=self.kwargs['project_id'])

            project_visits = ProjectVisits.objects.get(project=project)
            project_visits.visits = project_visits.visits + 1
            project_visits.save(force_update=True)

            return project
        else:
            return None

    def destroy(self, request, *args, **kwargs):
        auth = authenticate(request)

        if auth:
            instance = self.get_object()
            dir_to_delete = 'uploads/' + str(instance.id)
            shutil.rmtree(dir_to_delete)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return None


class ProjectCSV(ListCreateAPIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        auth = authenticate(self.request)

        if auth:
            temporary_uuid = uuid4()

            file_obj = request.data['file']
            # parse and convert de the file
            data_set = file_obj.read().decode('UTF-8')
            io_string = io.StringIO(data_set)

            # create the csv file
            with open('temporary_csv/' + str(temporary_uuid) + '.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                    writer.writerow(column)

            df = pd.read_csv('temporary_csv/' + str(temporary_uuid) +
                             '.csv', error_bad_lines=False).fillna('')
            return Response({'temporary_uuid': str(temporary_uuid), 'columns': df.columns}, status=200)
        else:
            return None


class ProjectConfigurationViewSet(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectConfigurationSerializer

    def get_object(self, queryset=None):
        auth = authenticate(self.request)

        if auth:
            project_configuration = ProjectConfiguration.objects.get(
                project_id=self.kwargs['project_id'], id=self.kwargs['configuration_id'])
            return project_configuration
        else:
            return None


class ProjectConfigurationCreateViewSet(ListCreateAPIView):
    serializer_class = ProjectConfigurationSerializer

    def get_object(self, queryset=None):
        auth = authenticate(self.request)

        if auth:
            project_configuration = ProjectConfiguration.objects.get(
                project_id=self.kwargs['project_id'])
            return project_configuration
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
                project = serializer.save()
                result_dict = ProjectConfigurationSerializer(project).data
        else:
            result_status = status.HTTP_401_UNAUTHORIZED
            result_status["reasons"] = 'Not authorized'

        return Response(result_dict, status=result_status)


class ProjectConfigurationFilesCreateViewSet(ListCreateAPIView):
    serializer_class = ProjectFilesSerializer

    def get_object(self, queryset=None):
        user = authenticate(self.request)

        if user:
            configuration_file = ProjectConfigFile.objects.get(
                project_configuration_id=self.kwargs['configuration_id'])
            return configuration_file
        else:
            return None

    def post(self, request, *args, **kwargs):
        auth = authenticate(request)
        result_status = status.HTTP_201_CREATED
        result_dict = {}

        if auth:
            file_url = request.data['project_id'] + \
                '/' + request.data['project_configuration']
            request.data['file_url'] = file_url
            temporary_uuid = request.data['temporary_uuid']
            from_database = request.data['from_database']
            serializer = self.get_serializer(data=request.data)

            if not serializer.is_valid():
                result_status = status.HTTP_400_BAD_REQUEST
                result_dict["reasons"] = serializer.errors
            else:
                try:
                    project_configuration_id = self.kwargs['configuration_id']
                    project_configuration = ProjectConfiguration.objects.get(
                        id=project_configuration_id)

                    token = sub('Token ', '', self.request.META.get(
                        'HTTP_AUTHORIZATION', None))

                    task = train_regression_model.delay(
                        request=request.data,
                        project_configuration_id=project_configuration_id,
                        temporary_uuid=temporary_uuid,
                        token=token,
                        account_type=auth.account_type,
                        from_database=from_database,
                    )

                    project_configuration.training_task_id = task.id
                    project_configuration.training_task_status = task.state
                    project_configuration.last_time_trained = timezone.now()
                    project_configuration.created_from_database = from_database
                    project_configuration.save(force_update=True)
                except ValueError:
                    print(ValueError)

        else:
            result_status = status.HTTP_401_UNAUTHORIZED
            result_status["reasons"] = 'Not authorized'

        return Response(result_dict, status=result_status)


class ProjectConfigurationFilesViewSet(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectFilesSerializer

    def get_object(self, queryset=None):
        user = authenticate(self.request)

        if user:
            configuration_file = ProjectConfigFile.objects.get(
                id=self.kwargs['configuration_file_id'], configuration_file_id=self.kwargs['configuration_id'])

            return configuration_file
        else:
            return None


class ProjectModelAPI(CreateAPIView):
    def post(self, request, *args, **kwargs):
        user = authenticate(self.request)

        if user:
            project_id = self.kwargs['project_id']
            project_config = ProjectConfiguration.objects.get(
                project_id=project_id)
            project_config_file = ProjectConfigFile.objects.get(
                project_configuration=project_config)
            model_url = project_config_file.file_url

            model = joblib.load(model_url + '/model.joblib')
            values = request.data['values']
            np_values = np.array(list(values.values()))
            converted_values = np.array(
                [[round(float(item)) for item in np_values]])

            prediction = model.predict(converted_values)

            return Response({"prediction": prediction[0]}, status=200)
        else:
            return None
