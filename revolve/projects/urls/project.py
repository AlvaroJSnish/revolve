from django.urls import re_path
from projects.views import ProjectsViewSet, ProjectViewSet, ProjectConfigurationViewSet, ProjectConfigurationFilesCreateViewSet

urlpatterns = [
    re_path(r'^projects/?$', ProjectsViewSet.as_view(), name="projects"),
    re_path(r'^projects/(?P<project_id>[0-9_a-zA-Z\-]+)?$', ProjectViewSet.as_view(),
            name="project_configuration_create"),
    re_path(r'^projects/(?P<project_id>[0-9_a-zA-Z\-]+)/config/(?P<configuration_id>[0-9_a-zA-Z\-]+)?$', ProjectConfigurationViewSet.as_view(),
            name="project_configuration_retrieve_update_delete"),
    re_path(r'^projects/(?P<project_id>[0-9_a-zA-Z\-]+)/config/(?P<configuration_id>[0-9_a-zA-Z\-]+)/config_file?$', ProjectConfigurationFilesCreateViewSet.as_view(),
            name="project_configuration_file")
]
