from uuid import uuid4

from django.db import models

from common.base_models import BaseModel
from databases.models import Database
from projects.models import Project
from users.models import User


class Retrain(BaseModel):
    name = 'Retrain'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_retrain')
    database = models.ForeignKey(
        Database, on_delete=models.CASCADE, related_name='database_retrain')
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='project_retrain')
    scheduled = models.BooleanField(default=False)
    scheduled_every = models.IntegerField(null=True, choices=((5, 5), (7, 7), (14, 14), (31, 31)))
    task_id = models.UUIDField(default=uuid4)
