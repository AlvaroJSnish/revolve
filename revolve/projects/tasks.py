import json
import os

import numpy as np
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone

from celery import shared_task
from common.serializers import UUIDEncoder
from common.timer import Timer
from common.token import sync_user_by_token
from dataframes import Dataframe
from nn_models import BasicLinearModel
from projects.models import ProjectConfiguration
from projects.serializers import ProjectSerializer
from stats.models import Stat
from userstats.models import UserStats

channel_layer = get_channel_layer()


@shared_task(name="Basic Regression Model Training")
def train_regression_model(request, project_configuration_id, temporary_uuid, token):
    try:
        os.makedirs('uploads/' + request['file_url'])
        p_path = 'uploads/' + request['file_url']

        label = request['label']
        all_columns = np.array(request['all_columns'])
        deleted_columns = np.array(request['deleted_columns'])

        csv_path = 'temporary_csv/' + temporary_uuid + '.csv'

        dataframe = Dataframe(csv_path, all_columns, deleted_columns, label, p_path, project_configuration_id)
        df_features, df_labels = dataframe.get_transformed_data()

        timer = Timer()
        timer.start()

        model = BasicLinearModel(df_features, df_labels, p_path)
        model.train_and_save()
        error, accuracy = model.get_metrics()

        elapsed_time = timer.stop()

        # modify project config
        project_configuration = ProjectConfiguration.objects.get(id=project_configuration_id)
        project_configuration.trained = True
        project_configuration.last_time_trained = timezone.now()
        project_configuration.accuracy = accuracy
        project_configuration.error = error
        project_configuration.training_task_status = 'SUCCESS'
        project_configuration.save(force_update=True)

        # pass info to websocket
        async_to_sync(channel_layer.group_send)(
            token,
            {
                'type': 'updated_project',
                'message': json.dumps(ProjectSerializer(project_configuration.project).data, cls=UUIDEncoder)
            }
        )

        # create stats
        Stat.objects.create(project_type=project_configuration.project_type, project_plan='BASIC',
                            features_columns=len(df_features), elapsed_time=elapsed_time,
                            trained_date=timezone.now())
        user = sync_user_by_token(token)
        user_stats = UserStats.objects.get(user=user)
        user_stats.regression_models_trained = user_stats.regression_models_trained + 1
        user_stats.average_accuracy = (user_stats.average_accuracy + accuracy) / (
                user_stats.regression_models_trained + user_stats.classification_models_trained)
        user_stats.average_error = (user_stats.average_error + error) / (
                user_stats.regression_models_trained + user_stats.classification_models_trained)
        user_stats.save(force_update=True)

    except ValueError:
        project_configuration = ProjectConfiguration.objects.get(id=project_configuration_id)
        os.removedirs('uploads/' + request['file_url'])
        project_configuration.trained = False
        project_configuration.last_time_trained = timezone.now()
        project_configuration.training_task_status = 'REVOKED'
        project_configuration.save(force_update=True)
