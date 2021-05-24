from rest_framework.serializers import ModelSerializer

from databases.serializers import UsersSerializer, DatabaseLiteSerializer
from groups.models import Group
from projects.serializers import ProjectLiteSerializer
from users.serializers import UserLiteSerializer


class GroupsSerializer(ModelSerializer):
    owner = UsersSerializer(many=False)

    class Meta:
        model = Group
        fields = ('id', 'owner', 'group_name')


class GroupCreateSerializer(ModelSerializer):
    owner = UsersSerializer(many=False, required=False)

    class Meta:
        model = Group
        fields = ('id', 'group_name', 'owner')
        read_only_fields = ('owner',)

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        return Group.objects.create(owner=user, **validated_data)


class GroupSerializer(ModelSerializer):
    owner = UsersSerializer(many=False)
    users = UserLiteSerializer(many=True, required=False)
    databases = DatabaseLiteSerializer(many=True, required=False)
    projects = ProjectLiteSerializer(many=True, required=False)

    class Meta:
        model = Group
        fields = ('id', 'owner', 'users', 'databases', 'invitation_code', 'group_name', 'projects')

    def destroy(self, request, *args, **kwargs):
        group_id = self.context['view'].kwargs.get('group_id')
