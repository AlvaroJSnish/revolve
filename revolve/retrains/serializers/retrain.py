from rest_framework.serializers import ModelSerializer

from databases.serializers import DatabaseSerializer
from projects.serializers import ProjectSerializer
from retrains.models import Retrain
from users.serializers import UsersSerializer


class RetrainCreateSerializer(ModelSerializer):
    owner = UsersSerializer(read_only=True)
    database = DatabaseSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Retrain
        fields = (
            'id', 'owner', 'project', 'database', 'scheduled_every', 'scheduled', 'task_id',)

    def create(self, validated_data):
        user = None

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        if request.data['from_database']:
            return Retrain.objects.create(owner=user,
                                          database_id=request.data['database'],
                                          project_id=request.data['project'],
                                          scheduled=True,
                                          scheduled_every=request.data['days'],
                                          **validated_data)

        return Retrain.objects.create(owner=user, project_id=request.data['project'])
