import pandas as pd
from django.contrib.postgres.fields import ArrayField
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, SerializerMethodField

from projects.models import Project, ProjectConfiguration, ProjectConfigFile
from users.serializers import UsersSerializer


class ProjectFilesSerializer(ModelSerializer):
    project_configuration = PrimaryKeyRelatedField(
        read_only=True, many=False)
    file_url = serializers.CharField()
    all_columns = ArrayField(serializers.CharField())
    saved_columns = ArrayField(serializers.CharField())
    deleted_columns = ArrayField(serializers.CharField(), blank=True)
    final_data = ArrayField(ArrayField(serializers.CharField()))
    label = serializers.CharField()

    class Meta:
        model = ProjectConfigFile
        fields = ('id', 'project_configuration', 'file_url',
                  'all_columns', 'saved_columns', 'deleted_columns', 'label', 'final_data')


class ProjectConfigurationSerializer(ModelSerializer):
    correlation = SerializerMethodField('get_correlation')
    project = PrimaryKeyRelatedField(read_only=True, many=False)

    TYPE_CHOICES = (("CLASSIFICATION", 'Clasificación'),
                    ("REGRESSION", "Regresión"))

    STATUS_CHOICES = (('PENDING', 'Pendiente'),
                      ('STARTED', 'Empezada'),
                      ('RETRY', 'Reintentando'),
                      ('SUCCESS', 'Finalizado'),
                      ('REVOKED', 'Rechazado'),
                      ('RECEIVED', 'Recibido'),
                      ('FAILURE', 'Fallida'))

    configuration_file = ProjectFilesSerializer(
        read_only=True, many=False, required=False)
    project_type = serializers.ChoiceField(
        choices=TYPE_CHOICES,
    )
    trained = serializers.BooleanField(required=False)
    last_time_trained = serializers.DateTimeField(required=False)
    accuracy = serializers.FloatField(required=False)
    error = serializers.FloatField(required=False)
    training_task_id = serializers.UUIDField(required=False)
    training_task_status = serializers.ChoiceField(choices=STATUS_CHOICES, required=False)

    class Meta:
        model = ProjectConfiguration
        fields = ('id', 'project_type', 'project',
                  'trained', 'last_time_trained', 'configuration_file', 'accuracy', 'error', 'training_task_id',
                  'training_task_status', 'correlation',)
        read_only_fields = ('id', 'configuration_file', 'project')

    def get_correlation(self, obj):
        project_id = str(obj.project.id)
        project_config = str(obj.id)
        csv = 'uploads/' + project_id + '/' + project_config + '/dataframe.csv'
        dataframe = pd.read_csv(csv)
        return dataframe.corrwith(dataframe[obj.configuration_file.label]).to_dict()

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
