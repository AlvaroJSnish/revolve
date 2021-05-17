from django.contrib.auth import authenticate
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from userstats.models import UserStats
from userstats.serializers import UserStatSerializer


class UserStatsViewSet(RetrieveUpdateDestroyAPIView):
    serializer_class = UserStatSerializer

    def get_object(self, queryset=None):
        auth = authenticate(self.request)

        if auth:
            user_stats = UserStats.objects.get(user=self.kwargs['user_id'])
            return user_stats
        else:
            return None
