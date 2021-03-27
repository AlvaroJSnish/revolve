from django.core.validators import int_list_validator
from django.utils.translation import gettext_lazy as _
from django.db import models
from uuid import uuid4

from common.base_models import BaseModel
from users.models.user import User


class Project(BaseModel):
    name = 'Project'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project_name = models.CharField(max_length=100, default="Mi proyecto")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_project')

    def delete(self):
        if self.project_configuration:
            self.project_configuration.delete()
        super(Project, self).delete()


class ProjectConfiguration(BaseModel):
    name = 'ProjectConfiguration'

    class ProjectType(models.TextChoices):
        CLASSIFICATION = 'Clasificación', _('Clasificación')
        REGRESSION = 'Regresión', _('Regresión')

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, related_name='project_configuration', null=True)
    project_type = models.CharField(
        max_length=40,
        choices=ProjectType.choices,
        default=ProjectType.CLASSIFICATION,
    )
    trained = models.BooleanField(default=False)
    last_time_trained = models.DateTimeField(blank=True, null=True)
