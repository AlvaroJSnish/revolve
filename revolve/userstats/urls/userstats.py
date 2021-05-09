from django.urls import re_path

from userstats.views import UserStatsViewSet

urlpatterns = [
    re_path(r'^userstats/(?P<user_id>[0-9_a-zA-Z\-]+)?$', UserStatsViewSet.as_view(),
            name="userstats"),
]
