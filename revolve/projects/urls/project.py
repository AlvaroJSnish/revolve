from django.urls import re_path

from projects.views import ProjectsViewSet, ProjectViewSet, ProjectConfigurationCreateViewSet, \
    ProjectConfigurationViewSet, ProjectConfigurationFilesCreateViewSet, ProjectConfigurationFilesViewSet, ProjectCSV, \
    ProjectModelAPI, ProjectFromDatabase

urlpatterns = [
    re_path(r'^projects/?$', ProjectsViewSet.as_view(), name="projects"),
    re_path(r'^projects/(?P<project_id>[0-9_a-zA-Z\-]+)?$', ProjectViewSet.as_view(),
            name="project"),
    re_path(r'^projects/(?P<project_id>[0-9_a-zA-Z\-]+)/predict?$', ProjectModelAPI.as_view(),
            name="project_prediction"),
    re_path(r'^projects/(?P<project_id>[0-9_a-zA-Z\-]+)/config?$', ProjectConfigurationCreateViewSet.as_view(),
            name="project_configuation_create"),
    re_path(r'^projects/(?P<project_id>[0-9_a-zA-Z\-]+)/config/(?P<configuration_id>[0-9_a-zA-Z\-]+)?$',
            ProjectConfigurationViewSet.as_view(),
            name="project_configuration_retrieve_update_delete"),
    re_path(r'^projects/(?P<project_id>[0-9_a-zA-Z\-]+)/config/(?P<configuration_id>[0-9_a-zA-Z\-]+)/config_file?$',
            ProjectConfigurationFilesCreateViewSet.as_view(),
            name="project_configuration_file_create"),
    re_path(
        r'^projects/(?P<project_id>[0-9_a-zA-Z\-]+)/config/(?P<configuration_id>[0-9_a-zA-Z\-]+)/config_file/(?P<configuration_file_id>[0-9_a-zA-Z\-]+)?$',
        ProjectConfigurationFilesViewSet.as_view(),
        name="project_configuration_file_retreive_update_delete"),
    ## experimental
    re_path(r'^project-file/?$', ProjectCSV.as_view(), name="project-csv"),
    re_path(r'^projects/(?P<project_id>[0-9_a-zA-Z\-]+)/config/(?P<configuration_id>[0-9_a-zA-Z\-]+)/database?$',
            ProjectFromDatabase.as_view(),
            name="project_from_database"),
]
