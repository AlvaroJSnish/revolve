from rest_framework.serializers import ModelSerializer

from stats.models.stat import Stat


class StatSerializer(ModelSerializer):
    class Meta:
        model = Stat
        fields = ('id', 'project_type', 'project_plan', 'features_columns', 'elapsed_time', 'trained_date')
        read_only_fields = ('id',)
