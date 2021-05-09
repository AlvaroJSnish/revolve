from rest_framework.generics import RetrieveUpdateDestroyAPIView

from userstats.models import UserStats
from userstats.serializers import UserStatSerializer


class UserStatsViewSet(RetrieveUpdateDestroyAPIView):
    serializer_class = UserStatSerializer

    def get_object(self, queryset=None):
        user_stats = UserStats.objects.get(user=self.kwargs['user_id'])
        return user_stats
        # auth = authenticate(request)
        # if auth:
        #     if not serializer.is_valid():
        #         result_status = status.HTTP_400_BAD_REQUEST
        #         result_dict["reasons"] = serializer.errors
        #     else:
        #         project = serializer.save()
        #         result_dict = ProjectConfigurationSerializer(project).data
        # else:
        #     result_status = status.HTTP_401_UNAUTHORIZED
        #     result_status["reasons"] = 'Not authorized'
