from django.urls import re_path

from groups.views import GroupsViewSet

urlpatterns = [
    re_path(r'^groups/?$', GroupsViewSet.as_view(), name="groups"), ]
