from uuid import uuid4

from django.db import models
from django.utils import timezone


class SoftDeletionManager(models.Manager):
    class SoftDeletionQuerySet(models.QuerySet):

        def delete(self):
            return super(SoftDeletionManager.SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

        def hard_delete(self):
            return super(SoftDeletionManager.SoftDeletionQuerySet, self).delete()

        def alive(self):
            return self.filter(deleted_at=None)

        def dead(self):
            return self.exclude(deleted_at=None)

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionManager.SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionManager.SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()


class SensibleDataModel(SoftDeletionModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class BaseModel(SoftDeletionModel):
    class Meta:
        abstract = True
        ordering = ['-updated_at']

    def __str__(self):
        return self.name
