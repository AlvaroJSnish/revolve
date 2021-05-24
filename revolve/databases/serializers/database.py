from rest_framework.serializers import ModelSerializer

from databases.models import Database
from users.serializers import UsersSerializer


class DatabaseSerializer(ModelSerializer):
    owner = UsersSerializer(read_only=True)

    class Meta:
        model = Database
        fields = (
            'id', 'owner', 'database_name', 'database_type',)
        read_only_fields = ('id', 'owner',)

    def destroy(self, request, *args, **kwargs):
        database_id = self.context['view'].kwargs.get('database_id')


class DatabasesLiteSerializer(ModelSerializer):
    class Meta:
        model = Database
        fields = ('id', 'database_name',)
        read_only_fields = ('id', 'database_name',)


class DatabasesSerializer(ModelSerializer):
    owner = UsersSerializer(read_only=True)

    class Meta:
        model = Database
        fields = (
            'id', 'owner', 'database_name', 'database_type', 'database_port', 'database_host', 'database_password',
            'database_user')
        read_only_fields = ('id', 'owner',)

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        return Database.objects.create(owner=user, **validated_data)


class DatabaseLiteSerializer(ModelSerializer):
    class Meta:
        model = Database
        fields = ('id', 'database_name')
        read_only_fields = ('id', 'database_name')
