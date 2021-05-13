from django.urls import re_path

from databases.views import DatabasesViewSet, DatabaseViewSet

urlpatterns = [
    re_path(r'^databases/?$', DatabasesViewSet.as_view(), name="databases"),
    re_path(r'^databases/(?P<project_id>[0-9_a-zA-Z\-]+)?$', DatabaseViewSet.as_view(),
            name="database"),
]
