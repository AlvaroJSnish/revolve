import json
from datetime import datetime, timedelta

from channels.layers import get_channel_layer

from celery import shared_task
from common.serializers import UUIDEncoder
from common.timer import Timer
from databases.classes import DatabaseConnector
from databases.models import Database
from dataframes import DataframeFromDB
from nn_models import BasicLinearModel
from projects.models import Project, ProjectConfigFile
from projects.models import ProjectConfiguration
from projects.serializers import ProjectSerializer
from projects.tasks import call_socket, update_project_configuration, create_stats

channel_layer = get_channel_layer()


# from datetime import datetime, timedelta


@shared_task(name="Basic Regression Model Retraining")
def retrain_basic_regression_model(request, project_id, token):
    project = Project.objects.get(id=project_id)
    project_config = ProjectConfiguration.objects.get(project=project)
    project_config_file = ProjectConfigFile.objects.get(project_configuration=project_config)

    if project_config.created_from_database:
        database = Database.objects.get(id=project_config.database.id)
        model_url = project_config_file.file_url

        table_name = project.project_name
        db_connector = DatabaseConnector(
            database_host=database.database_host,
            database_name=database.database_name,
            database_port=database.database_port,
            database_type=database.database_type,
            database_user=database.database_user,
            database_password=database.database_password,
        )

        db_connector.connect()

        # query = f'select * from {table_name} except all select * from revolve_{table_name}_records'
        query = f'select * from {table_name}'

        results = db_connector.execute_query(query)
        db_connector.disconnect()

        dataframe = DataframeFromDB(
            data=results,
            all_columns=project_config_file.all_columns,
            deleted_columns=project_config_file.deleted_columns,
            project_configuration_id=project_config.id,
            label=project_config_file.label,
            path=model_url,
            is_retrain=True
        )

        df_features, df_labels = dataframe.get_transformed_data()

        timer = Timer()
        timer.start()
        model = BasicLinearModel(df_features, df_labels, model_url)
        model.train_and_save()
        error, accuracy = model.get_metrics()
        elapsed_time = timer.stop()

        # modify project config
        project_configuration = update_project_configuration(project_config.id, error, accuracy, database)

        # pass info to websocket
        call_socket(message_type='updated_project',
                    message_data=json.dumps(ProjectSerializer(project_configuration.project).data,
                                            cls=UUIDEncoder), token=token)

        # create stats
        create_stats(project_configuration=project_configuration, df_features=df_features,
                     elapsed_time=elapsed_time, error=error, accuracy=accuracy, token=token)

        time = datetime.utcnow() + timedelta(days=int(request['days']))
        retrain_basic_regression_model.apply_async(args=[request, project_id, token], eta=time)
