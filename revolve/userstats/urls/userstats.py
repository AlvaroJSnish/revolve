from django.urls import re_path

from userstats.views import UserStatsViewSet

urlpatterns = [
    re_path(r'^userstats/?$', UserStatsViewSet.as_view(),
            name="userstats"),
]
