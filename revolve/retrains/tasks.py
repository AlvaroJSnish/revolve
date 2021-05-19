from datetime import datetime, timedelta

from celery import shared_task


# from projects.models import Project


@shared_task(name="Basic Regression Model Retraining")
def retrain_basic_regression_model(request, project):
    # project = Project.objects.get(id=project_id)
    # db_connector = DatabaseConnector()

    # retrain_basic_regression_model.apply_async(
    #     (request.data, project.id),
    #     eta=time)

    time = datetime.utcnow() + timedelta(days=int(request['days']))
    retrain_basic_regression_model.apply_async(args=[request, None], eta=time)

    pass
