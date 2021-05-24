from uuid import uuid4

from django.db import models

from common.base_models import BaseModel
from databases.models import Database
from projects.models import Project
from users.models import User


class Group(BaseModel):
    name = 'Group'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    group_name = models.TextField(blank=False, null=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='group_owner')
    users = models.ManyToManyField(User, related_name='group_databases')
    databases = models.ManyToManyField(Database, related_name='group_databases')
    projects = models.ManyToManyField(Project, related_name='group_projects')
    invitation_code = models.UUIDField(default=uuid4)
