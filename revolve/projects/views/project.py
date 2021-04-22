import os
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import xgboost
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.response import Response
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.model_selection import train_test_split, StratifiedKFold, RandomizedSearchCV

from common.serializers import GenericPaginationSerializer
from common.utils import transform_values, transform_label
from projects.models import Project, ProjectConfiguration, ProjectConfigFile
from projects.serializers import ProjectSerializer, ProjectConfigurationSerializer, ProjectFilesSerializer

UPLOAD_DIR = '../../uploads/'


class ProjectsViewSet(ListCreateAPIView):
    serializer_class = ProjectSerializer
    pagination_class = GenericPaginationSerializer

    def get_queryset(self):
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
                try:
                    # create the dir to save files
                    os.makedirs('uploads/' + request.data['file_url'])
                    p_path = 'uploads/' + request.data['file_url']

                    # get the data from the request
                    data = request.data['final_data']
                    label = request.data['label']
                    all_columns = np.array(request.data['all_columns'])
                    saved_columns = np.array(request.data['saved_columns'])
                    deleted_columns = np.array(request.data['deleted_columns'])

                    # create the dataframe
                    dataframe = pd.DataFrame(
                        data=data, columns=all_columns, index=None)

                    # drop columns listed on deleted_columns
                    for column in all_columns:
                        if np.isin(column, deleted_columns):
                            dataframe.drop(column, inplace=True, axis=1)

                    # features and labels
                    dataframe_features = dataframe.drop(label, axis=1)
                    dataframe_labels = dataframe[label].copy()

                    # transform the values
                    transformed_dataframe_features = transform_values(dataframe_features)
                    transformed_dataframe_labels = transform_label(dataframe_labels)

                    test_size = 0.2
                    X_train, X_test, y_train, y_test = train_test_split(
                        transformed_dataframe_features, transformed_dataframe_labels, test_size=test_size)

                    # save data to files
                    # label_correlation.to_csv(
                    #     p_path + "/correlation.csv")  #  correlation
                    # X_train.to_csv(
                    #     p_path + "/transformed_dataframe_features.csv", index=False)  # dataframe features
                    # y_train.to_csv(
                    #     p_path + "/transformed_dataframe_labels.csv", index=False)  # dataframe label
                    # dataframe.to_csv(
                    #     p_path + "/dataframe_final.csv", index=False)
                    # np.savetxt(p_path + "/dataframe_transformed.csv",
                    #            transformed_dataframe, delimiter=',')

                    # model training
                    # A parameter grid for XGBoost
                    params = {
                        'min_child_weight': [1, 3, 5, 7, 10],
                        'gamma': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.5, 2, 5],
                        'subsample': [0.6, 0.8, 1.0],
                        'colsample_bytree': [0.3, 0.4, 0.6, 0.8, 1.0],
                        'max_depth': [3, 4, 5, 6, 8, 10, 12, 15, 17, 19, 21],
                        'learning_rate': [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
                    }
                    folds = 50
                    param_comb = 6
                    random_state = 1001
                    n_estimators = 250
                    n_thread = 1
                    n_jobs = 4

                    skf = StratifiedKFold(
                        n_splits=folds, shuffle=True, random_state=random_state)

                    xgb = xgboost.XGBRegressor(n_estimators=n_estimators, nthread=n_thread)
                    model = RandomizedSearchCV(xgb, param_distributions=params, n_iter=param_comb, n_jobs=n_jobs,
                                               cv=skf.split(
                                                   X_train, y_train), verbose=3, random_state=random_state)

                    model.fit(X_train, y_train)

                    joblib.dump(model.best_estimator_, p_path + '/model.joblib')

                    # testing
                    y_pred = model.predict(X_test)
                    mse = mean_squared_error(y_test, y_pred)
                    predictions = [round(value) for value in y_pred]
                    accuracy = accuracy_score(y_test, predictions)

                    p_file = serializer.save(
                        project_configuration_id=self.kwargs['configuration_id'])
                    p_config = ProjectConfiguration.objects.get(
                        id=self.kwargs['configuration_id'])
                    p_config.trained = True
                    p_config.last_time_trained = datetime.now()
                    p_config.accuracy = accuracy
                    p_config.error = mse
                    p_config.save(force_update=True)

                    result_dict = ProjectFilesSerializer(p_file).data
                except ValueError:
                    os.removedirs('uploads/' + request.data['file_url'])

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
