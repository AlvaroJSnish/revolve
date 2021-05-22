from django.urls import re_path

from users.views.users import UsersViewSet, CheckUserProjects, CheckUserDatabases, CheckUserGroups

urlpatterns = [
    re_path(r'list/', UsersViewSet.as_view(), name="users"),
    re_path(r'^available-projects/?$', CheckUserProjects.as_view(), name="user_projects_slots"),
    re_path(r'^available-databases/?$', CheckUserDatabases.as_view(), name="user_databases_slots"),
    re_path(r'^available-groups/?$', CheckUserGroups.as_view(), name="user_groups_slots"),
]
