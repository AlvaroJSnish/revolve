from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.response import Response

from projects.models import Project, ProjectConfiguration
from projects.serializers import ProjectSerializer, ProjectConfigurationSerializer
from common.serializers import GenericPaginationSerializer


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

    # def get(self, request, *args, **kwargs):
    #     result_status = status.HTTP_200_OK
    #     result_dict = {}

    #     user = authenticate(self.request)

    #     if user is not None:
    #         project_id = self.kwargs['project_id']

    #         try:
    #             project_configuration = ProjectConfiguration.objects.get(
    #                 id=project_id)
    #             if project_configuration is not None:
    #                 result_status = status.HTTP_200_OK
    #                 result_dict = {
    #                     "id": project_configuration.id,
    #                     "project": project_configuration.project.id,
    #                     "project_type": project_configuration.project_type,
    #                     "trained": project_configuration.trained,
    #                     "last_time_trained": project_configuration.last_time_trained
    #                 }
    #             else:
    #                 result_status = status.HTTP_400_BAD_REQUEST
    #                 result_dict['reasons'] = 'ID inválido'
    #         except:
    #             result_status = status.HTTP_400_BAD_REQUEST
    #             result_dict['reason'] = 'ID inválido'
    #             return Response(result_dict, status=result_status)

    #     return Response(result_dict, status=result_status)

    # def patch(self, request, *args, **kwargs):
    #     result_status = status.HTTP_200_OK
    #     result_dict = {}

    #     user = authenticate(self.request)

    #     if user is not None:
    #         project_id = self.kwargs['project_id']

    #         try:
    #             project_configuration = ProjectConfiguration.objects.get(
    #                 id=project_id)
    #             if project_configuration is not None:
    #                 print("--------------------------------")
    #                 print(request.POST.keys())
    #                 print("--------------------------------")
    #                 # project_configuration.save()
    #                 pass
    #                 # project_configuration = ProjectConfiguration.objects.update(
    #                 #     self.kwargs, id=project_id)
    #                 # result_status = status.HTTP_200_OK
    #                 # result_dict = {
    #                 #     "id": project_configuration.id,
    #                 #     "project": project_configuration.project.id,
    #                 #     "project_type": project_configuration.project_type,
    #                 #     "trained": project_configuration.trained,
    #                 #     "last_time_trained": project_configuration.last_time_trained
    #                 # }
    #             else:
    #                 result_status = status.HTTP_400_BAD_REQUEST
    #                 result_dict['reasons'] = 'ID inválido'
    #         except:
    #             result_status = status.HTTP_400_BAD_REQUEST
    #             result_dict['reason'] = 'ID inválido'
    #             return Response(result_dict, status=result_status)

    #     return Response(result_dict, status=result_status)
