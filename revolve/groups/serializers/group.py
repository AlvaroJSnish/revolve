from rest_framework.serializers import ModelSerializer

from databases.serializers import UsersSerializer, DatabasesSerializer
from groups.models import Group
from projects.serializers import ProjectSerializer


class GroupsSerializer(ModelSerializer):
    owner = UsersSerializer(many=False)

    class Meta:
        model = Group
        fields = ('id', 'owner', 'group_name')


class GroupCreateSerializer(ModelSerializer):
    owner = UsersSerializer(many=False)

    class Meta:
        model = Group
        fields = ('id', 'group_name', 'owner')

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        return Group.objects.create(owner=user, **validated_data)


class GroupSerializer(ModelSerializer):
    owner = UsersSerializer(many=False)
    users = UsersSerializer(many=True, required=False)
    databases = DatabasesSerializer(many=True, required=False)
    projects = ProjectSerializer(many=True, required=False)

    class Meta:
        model = Group
        fields = ('id', 'owner', 'users', 'databases', 'invitation_code', 'group_name', 'projects')

    def destroy(self, request, *args, **kwargs):
        group_id = self.context['view'].kwargs.get('group_id')
