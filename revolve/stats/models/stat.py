from uuid import uuid4

from django.db import models

from common.base_models import BaseModel


class Stat(BaseModel):
    name = 'Stat'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project_type = models.CharField(max_length=100, blank=True, null=True)
    project_plan = models.CharField(max_length=100, blank=True, null=True)
    features_columns = models.CharField(max_length=100, blank=True, null=True)
    elapsed_time = models.FloatField(blank=True, null=True)
    trained_date = models.DateTimeField(blank=True, null=True)
