import datetime

from uuid import uuid4
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(**kwargs)

        if 'password' in kwargs:
            user.set_password(kwargs['password'])
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs["is_staff"] = True

        return self.create_user(**kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(
        max_length=90, null=False, blank=False, unique=True)
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    class Meta:
        abstract = False

    def set_password(self, raw_password):
        super(User, self).set_password(raw_password)
