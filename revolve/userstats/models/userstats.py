from uuid import uuid4

from django.db import models

from common.base_models import BaseModel
from projects.models.project import Project
from users.models.user import User


class UserStats(BaseModel):
    name = 'UserStat'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_stats')
    regression_models_trained = models.IntegerField(default=0, editable=True)
    classification_models_trained = models.IntegerField(default=0, editable=True)
    average_accuracy = models.FloatField(blank=True, null=True)
    average_error = models.FloatField(blank=True, null=True)
    last_week_average_accuracy = models.FloatField(blank=True, null=True)
    last_week_average_error = models.FloatField(blank=True, null=True)


class ProjectVisits(BaseModel):
    name = 'ProjectVisits'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='project_visits')
    visits = models.IntegerField(default=0, editable=True)
