from uuid import uuid4

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.base_models import BaseModel
from databases.models import Database
from users.models.user import User


class Project(BaseModel):
    name = 'Project'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project_name = models.CharField(max_length=100, default="Mi proyecto")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_project')
    finished = models.BooleanField(default=False)


class ProjectConfiguration(BaseModel):
    name = 'ProjectConfiguration'

    class ProjectType(models.TextChoices):
        CLASSIFICATION = 'Clasificación', _('Clasificación')
        REGRESSION = 'Regresión', _('Regresión')

    class TaskStatus(models.TextChoices):
        PENDING = 'Pendiente', _('Pendiente')
        STARTED = 'Empezada', _('Empezada')
        RETRY = 'Reintentando', _('Reintentando')
        SUCCESS = 'Finalizado', _('Finalizado')
        REVOKED = 'Rechazado', _('Rechazado')
        RECEIVED = 'Recibido', _('Recibido')
        FAILURE = 'Fallida', _('Fallida')

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, related_name='project_configuration')
    project_type = models.CharField(
        max_length=40,
        choices=ProjectType.choices,
        default=ProjectType.REGRESSION,
    )
    trained = models.BooleanField(default=False)
    last_time_trained = models.DateTimeField(blank=True, null=True)
    accuracy = models.FloatField(blank=True, null=True)
    error = models.FloatField(blank=True, null=True)
    training_task_id = models.UUIDField(blank=True, null=True)
    training_task_status = models.CharField(max_length=40, choices=TaskStatus.choices, default=TaskStatus.PENDING)
    configured_scheduled_training = models.BooleanField(default=False)
    created_from_database = models.BooleanField(default=False)
    database = models.OneToOneField(Database, on_delete=models.CASCADE, related_name='project_database', null=True)


class ProjectConfigFile(BaseModel):
    name = 'ProjectConfigFile'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project_configuration = models.OneToOneField(
        ProjectConfiguration, on_delete=models.CASCADE, related_name='configuration_file')
    file_url = models.TextField(blank=True, null=True)
    all_columns = ArrayField(
        models.CharField(max_length=200, blank=True), blank=True)
    saved_columns = ArrayField(
        models.CharField(max_length=200, blank=True), blank=True)
    deleted_columns = ArrayField(
        models.CharField(max_length=200, blank=True), blank=True)
    final_data = ArrayField(ArrayField(
        models.CharField(max_length=200, blank=True, null=True, default=""), blank=True, null=True), blank=True,
        null=True)
    final_label = ArrayField(models.CharField(max_length=200, blank=True, null=True, default=""), blank=True, null=True)
    label = models.CharField(max_length=200)
    # transformed_data = ArrayField(ArrayField(
    #     models.CharField(max_length=200, blank=True, null=True, default=""), blank=True, null=True), blank=True,
    #     null=True)
    # transformed_label = ArrayField(ArrayField(
    #     models.CharField(max_length=200, blank=True, null=True, default=""), blank=True, null=True), blank=True,
    #     null=True)
