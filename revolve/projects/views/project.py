import os
import pdb
import pandas as pd
import numpy as np

from joblib import dump
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.response import Response

from common.utils import transform_values
from common.serializers import GenericPaginationSerializer
from projects.models import Project, ProjectConfiguration, ProjectConfigFile
from projects.serializers import ProjectSerializer, ProjectConfigurationSerializer, ProjectFilesSerializer


UPLOAD_DIR = '../../uploads/'


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
                p_file = serializer.save(
                    project_configuration_id=self.kwargs['configuration_id'])

                os.makedirs('uploads/' + request.data['file_url'])
                p_path = 'uploads/' + request.data['file_url']

                data = request.data['final_data']
                label = request.data['label']
                all_columns = np.array(request.data['all_columns'])
                saved_columns = np.array(request.data['saved_columns'])
                deleted_columns = np.array(request.data['deleted_columns'])

                dataframe = pd.DataFrame(
                    data=data, columns=all_columns, index=None)

                # dataframe.info()

                for column in all_columns:
                    if np.isin(column, deleted_columns):
                        dataframe.drop(column, inplace=True, axis=1)

                dataframe.to_csv(p_path + "/data.csv", index=False)

                original_dataframe, transformed_dataframe = transform_values(
                    dataframe)

                # datos
                corr_matrix = original_dataframe.corr()
                quality_correlation = corr_matrix[label].sort_values(
                    ascending=False)

                quality_correlation.to_csv(p_path + "/correlation.csv")

                dataframe_features = original_dataframe.drop(
                    request.data['label'], axis=1)
                dataframe_labels = original_dataframe[request.data['label']].copy(
                )
                dataframe_features.to_csv(
                    p_path + "/transformed_dataframe_features.csv", index=False)
                dataframe_labels.to_csv(
                    p_path + "/transformed_dataframe_labels.csv", index=False)

                dataframe.to_csv(p_path + "/dataframe_final.csv", index=False)
                np.savetxt(p_path + "/dataframe_transformed.csv",
                           transformed_dataframe, delimiter=',')

                # model training
                lin_reg = LinearRegression()
                lin_reg.fit(transformed_dataframe, dataframe_labels)
                dump(lin_reg, p_path + "/model.joblib")

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
