from rest_framework.serializers import ModelSerializer

from users.models.user import User


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'avatar')
        read_only_fields = ('id',)


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
