from django.urls import re_path

from groups.views import GroupsViewSet, GroupViewSet, GroupAddDatabase, GroupAddProject, GroupAddUser

urlpatterns = [
    re_path(r'^groups/?$', GroupsViewSet.as_view(), name="groups"),
    re_path(r'^groups/(?P<group_id>[0-9_a-zA-Z\-]+)?$', GroupViewSet.as_view(),
            name="group"),
    re_path(r'^groups/(?P<group_id>[0-9_a-zA-Z\-]+)/add-project/(?P<project_id>[0-9_a-zA-Z\-]+)?$',
            GroupAddProject.as_view(),
            name="group_add_project"),
    re_path(r'^groups/(?P<group_id>[0-9_a-zA-Z\-]+)/add-database/(?P<database_id>[0-9_a-zA-Z\-]+)?$',
            GroupAddDatabase.as_view(),
            name="group_add_database"),
    re_path(r'^groups/(?P<group_id>[0-9_a-zA-Z\-]+)/add-user?$',
            GroupAddUser.as_view(),
            name="group_add_user"),
]
