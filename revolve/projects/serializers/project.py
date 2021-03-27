from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from users.serializers import UsersSerializer
from projects.models import Project, ProjectConfiguration


class ProjectConfigurationSerializer(ModelSerializer):
    class Meta:
        model = ProjectConfiguration
        fields = ('id', 'project_type',
                  'trained', 'last_time_trained')
        read_only_fields = ('id',)

    def create(self, validated_data):
        project_id = self.context['view'].kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        return ProjectConfiguration.objects.create(project=project, **validated_data)


class ProjectSerializer(ModelSerializer):
    owner = UsersSerializer(read_only=True)
    project_configuration = ProjectConfigurationSerializer(
        read_only=False, many=False, required=False)

    class Meta:
        model = Project
        fields = ('id', 'project_name', 'owner', 'project_configuration')
        read_only_fields = ('id', 'project_name', 'owner',)

    def create(self, validated_data):
        user = self.context['request'].user
        return Project.objects.create(owner=user, **validated_data)

    def destroy(self, request, *args, **kwargs):
        project_id = self.context['view'].kwargs.get('project_id')


class ProjectsSerializer(ModelSerializer):
    owner = UsersSerializer(read_only=True)
    project_configuration = ProjectConfigurationSerializer(
        read_only=False, many=False, required=False)

    class Meta:
        model = Project
        fields = ('id', 'owner', 'project_configuration')
        read_only_fields = ('id', 'owner',)
