import os

import numpy as np
from django.utils import timezone

from celery import shared_task
from common.timer import Timer
from dataframes import Dataframe
from nn_models import BasicLinearModel
from projects.models import ProjectConfiguration


@shared_task(name="Basic Regression Model Training")
def train_regression_model(request, project_configuration_id):
    try:
        os.makedirs('uploads/' + request['file_url'])
        p_path = 'uploads/' + request['file_url']

        data = request['final_data']
        label = request['label']
        all_columns = np.array(request['all_columns'])
        deleted_columns = np.array(request['deleted_columns'])

        dataframe = Dataframe(data, all_columns, deleted_columns, label)
        df_features, df_labels = dataframe.get_transformed_data()

        timer = Timer()
        timer.start()

        model = BasicLinearModel(df_features, df_labels, p_path)
        model.train_and_save()
        error, accuracy = model.get_metrics()

        elapsed_time = timer.stop()

        project_configuration = ProjectConfiguration.objects.get(id=project_configuration_id)

        project_configuration.trained = True
        project_configuration.last_time_trained = timezone.now()
        project_configuration.accuracy = accuracy
        project_configuration.error = error
        project_configuration.training_task_status = 'SUCCESS'
        project_configuration.save(force_update=True)

    except ValueError:
        project_configuration = ProjectConfiguration.objects.get(id=project_configuration_id)
        os.removedirs('uploads/' + request['file_url'])
        project_configuration.trained = False
        project_configuration.last_time_trained = timezone.now()
        project_configuration.training_task_status = 'REVOKED'
        project_configuration.save(force_update=True)
