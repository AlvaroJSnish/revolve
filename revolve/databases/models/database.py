from uuid import uuid4

from django.db import models
from django_cryptography.fields import encrypt

from common.base_models import BaseModel
from users.models import User


class Database(BaseModel):
    name = 'Database'

    class Types(models.TextChoices):
        POSTGRES = 'postgres'
        MYSQL = 'mysql'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    database_name = models.TextField()
    database_host = encrypt(models.TextField())
    database_port = encrypt(models.DecimalField(decimal_places=0, max_digits=6))
    database_user = encrypt(models.TextField(default="root"))
    database_password = encrypt(models.TextField())
    database_type = encrypt(models.TextField(choices=Types.choices, default=Types.POSTGRES))
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_database')
