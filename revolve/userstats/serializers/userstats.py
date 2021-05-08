from rest_framework.serializers import ModelSerializer

from projects.models import Project
from projects.serializers import ProjectSerializer
from users.serializers import UsersSerializer
from userstats.models import UserStats, ProjectVisits


class UserStatSerializer(ModelSerializer):
    user = UsersSerializer(
        read_only=False, many=True, required=False)

    class Meta:
        model = UserStats
        fields = ('id', 'user', 'regression_models_trained', 'classification_models_trained', 'average_accuracy',
                  'average_accuracy', 'last_week_average_accuracy', 'last_week_average_error')


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
