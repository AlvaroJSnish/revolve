from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.response import Response

from common.serializers import GenericPaginationSerializer
from projects.models import Project, ProjectConfiguration, ProjectConfigFile
from projects.serializers import ProjectSerializer, ProjectConfigurationSerializer, ProjectFilesSerializer


class ProjectsViewSet(ListCreateAPIView):
    serializer_class = ProjectSerializer
    pagination_class = GenericPaginationSerializer

    def get_queryset(self):
        result_status = status.HTTP_200_OK
        result_dict = {}

        filter_params = Q()

        user = authenticate(self.request)

        if user is not None:
            return Project.objects.filter(filter_params, owner=user).distinct().exclude(is_deleted=True)
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
                result_dict = ProjectSerializer(project).data
        else:
            result_status = status.HTTP_401_UNAUTHORIZED
            result_status["reasons"] = 'Not authorized'

        return Response(result_dict, status=result_status)


class ProjectViewSet(CreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    pagination_class = GenericPaginationSerializer

    def get_object(self, queryset=None):
        project = Project.objects.get(id=self.kwargs['project_id'])
        return project


class ProjectConfigurationViewSet(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectConfigurationSerializer

    def get_object(self, queryset=None):
        project_configuration = ProjectConfiguration.objects.get(
            project_id=self.kwargs['project_id'], id=self.kwargs['configuration_id'])
        return project_configuration


class ProjectConfigurationCreateViewSet(ListCreateAPIView):
    serializer_class = ProjectConfigurationSerializer

    def get_object(self, queryset=None):
        project_configuration = ProjectConfiguration.objects.get(
            project_id=self.kwargs['project_id'])
        return project_configuration

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
        configuration_file = ProjectConfigFile.objects.get(
            project_configuration_id=self.kwargs['configuration_id'])
        return configuration_file

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
                p_file = serializer.save(project_configuration_id=self.kwargs['configuration_id'])
                result_dict = ProjectFilesSerializer(p_file).data
        else:
            result_status = status.HTTP_401_UNAUTHORIZED
            result_status["reasons"] = 'Not authorized'

        return Response(result_dict, status=result_status)


class ProjectConfigurationFilesViewSet(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectFilesSerializer

    def get_object(self, queryset=None):
        configuration_file = ProjectConfigFile.objects.get(
            id=self.kwargs['configuration_file_id'], configuration_file_id=self.kwargs['configuration_id'])
        return configuration_file
