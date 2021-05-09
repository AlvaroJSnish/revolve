from django.utils import timezone
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from projects.models import Project, ProjectConfiguration
from projects.serializers import ProjectSerializer
from users.serializers import UsersSerializer
from userstats.models import UserStats, ProjectVisits


class UserStatSerializer(ModelSerializer):
    user = UsersSerializer(read_only=True)
    last_week_average_error = SerializerMethodField('get_last_week_average_error')
    last_week_average_accuracy = SerializerMethodField('get_last_week_average_accuracy')

    class Meta:
        model = UserStats
        fields = ('id', 'user', 'regression_models_trained', 'classification_models_trained', 'average_accuracy',
                  'average_error', 'last_week_average_error', 'last_week_average_accuracy')

    def get_last_week_average_error(self, obj):
        user = obj.user
        counter = 0
        last_week_average_error = 0
        projects = Project.objects.filter(owner=user).distinct().exclude(is_deleted=True)

        if projects and len(projects):
            for project in projects:
                if (timezone.now() - project.updated_at).days >= 7:
                    project_configuration = ProjectConfiguration.objects.get(project=project)
                    counter = counter + 1
                    last_week_average_error = (last_week_average_error + project_configuration.error) / counter

        return last_week_average_error

    def get_last_week_average_accuracy(self, obj):
        user = obj.user
        counter = 0
        last_week_average_accuracy = 0
        projects = Project.objects.filter(owner=user).distinct().exclude(is_deleted=True)

        if projects and len(projects):
            for project in projects:
                if (timezone.now() - project.updated_at).days >= 7:
                    project_configuration = ProjectConfiguration.objects.get(project=project)
                    counter = counter + 1
                    last_week_average_accuracy = (last_week_average_accuracy + project_configuration.accuracy) / counter

        return last_week_average_accuracy


class ProjectVisitsSerializer(ModelSerializer):
    project = ProjectSerializer(
        read_only=False, many=True, required=False)

    class Meta:
        model = ProjectVisits
        fields = ('id', 'project', 'visits')

    def create(self, validated_data):
        project_id = self.context['view'].kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        return ProjectVisits.objects.create(project=project, **validated_data)
