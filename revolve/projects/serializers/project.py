from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField


from users.serializers import UsersSerializer
from projects.models import Project, ProjectConfiguration, ProjectConfigFile


class ProjectFilesSerializer(ModelSerializer):
    project_configuration = PrimaryKeyRelatedField(
        read_only=True, many=False)
    file_url = serializers.CharField()
    all_columns = ArrayField(serializers.CharField())
    saved_columns = ArrayField(serializers.CharField())
    deleted_columns = ArrayField(serializers.CharField())
    final_data = ArrayField(serializers.CharField())
    label = serializers.CharField()

    class Meta:
        model = ProjectConfigFile
        fields = ('id', 'project_configuration', 'file_url',
                  'all_columns', 'saved_columns', 'deleted_columns', 'label')

        def create(self, validated_data):
            project_configuration_id = self.context['view'].kwargs.get(
                'project_configuration_id')
            project_configuration = Project.objects.get(
                id=project_configuration_id)
            return ProjectConfigFile.objects.create(project_configuration=project_configuration, **validated_data)


class ProjectConfigurationSerializer(ModelSerializer):
    TYPE_CHOICES = (("CLASSIFICATION", 'Clasificación'),
                    ("REGRESSION", "Regresión"))

    configuration_file = ProjectFilesSerializer(
        read_only=True, many=False)
    project_type = serializers.ChoiceField(
        choices=TYPE_CHOICES,
    )
    trained = serializers.BooleanField(required=False)
    last_time_trained = serializers.DateTimeField(required=False)

    class Meta:
        model = ProjectConfiguration
        fields = ('id', 'project_type',
                  'trained', 'last_time_trained', 'configuration_file')
        read_only_fields = ('id', 'configuration_file')

    def create(self, validated_data):
        project_id = self.context['view'].kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        return ProjectConfiguration.objects.create(project=project, **validated_data)


class ProjectSerializer(ModelSerializer):
    project_name = serializers.CharField(max_length=200)
    owner = UsersSerializer(read_only=True)
    project_configuration = ProjectConfigurationSerializer(
        read_only=False, many=True, required=False)

    class Meta:
        model = Project
        fields = ('id', 'project_name', 'owner', 'project_configuration')
        read_only_fields = ('id', 'project_name', 'owner',)

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        return Project.objects.create(owner=user, **validated_data)

    def destroy(self, request, *args, **kwargs):
        project_id = self.context['view'].kwargs.get('project_id')


class ProjectsSerializer(ModelSerializer):
    owner = UsersSerializer(read_only=True)
    project_configuration = ProjectConfigurationSerializer(
        read_only=False, many=True, required=False)

    class Meta:
        model = Project
        fields = ('id', 'owner', 'project_configuration')
        read_only_fields = ('id', 'owner',)
