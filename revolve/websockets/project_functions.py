from channels.db import database_sync_to_async

from projects.models import Project


# from projects.serializers import ProjectSerializer


@database_sync_to_async
def get_user_projects(user):
    return Project.objects.filter(owner=user).distinct().exclude(is_deleted=True)
