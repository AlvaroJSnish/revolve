from rest_framework.serializers import ModelSerializer

from databases.models import Database
from users.serializers import UsersSerializer


class DatabaseSerializer(ModelSerializer):
    owner = UsersSerializer(read_only=True)

    class Meta:
        model = Database
        fields = (
            'id', 'owner', 'database_name', 'database_host', 'database_port', 'database_password', 'database_type',
            'database_user')
        read_only_fields = ('id', 'owner',)

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        return Database.objects.create(owner=user, **validated_data)

    def destroy(self, request, *args, **kwargs):
        database_id = self.context['view'].kwargs.get('database_id')
