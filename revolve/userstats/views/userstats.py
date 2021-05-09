from rest_framework.generics import RetrieveUpdateDestroyAPIView

from userstats.models import UserStats
from userstats.serializers import UserStatSerializer


class UserStatsViewSet(RetrieveUpdateDestroyAPIView):
    serializer_class = UserStatSerializer

    def get_object(self, queryset=None):
        user_stats = UserStats.objects.get(user=self.kwargs['user_id'])
        return user_stats
