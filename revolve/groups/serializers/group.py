from rest_framework.serializers import ModelSerializer

from databases.serializers import UsersSerializer, DatabasesSerializer
from groups.models import Group
from projects.serializers import ProjectSerializer


class GroupSerializer(ModelSerializer):
    owner = UsersSerializer(many=False)
    users = UsersSerializer(many=True)
    databases = DatabasesSerializer(many=True)
    projects = ProjectSerializer(many=True)

    class Meta:
        model = Group
        fields = ('id', 'owner', 'users', 'databases', 'invitation_code', 'group_name', 'projects')
