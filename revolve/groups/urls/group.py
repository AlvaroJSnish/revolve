from django.urls import re_path

from groups.views import GroupsViewSet, GroupViewSet

urlpatterns = [
    re_path(r'^groups/?$', GroupsViewSet.as_view(), name="groups"),
    re_path(r'^groups/(?P<group_id>[0-9_a-zA-Z\-]+)?$', GroupViewSet.as_view(),
            name="group"),
]
