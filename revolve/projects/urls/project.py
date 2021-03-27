from django.urls import re_path
from projects.views import ProjectsViewSet, ProjectViewSet, ProjectConfigurationViewSet

urlpatterns = [
    re_path(r'^projects/?$', ProjectsViewSet.as_view(), name="projects"),
    re_path(r'^projects/(?P<project_id>[0-9_a-zA-Z\-]+)?$', ProjectViewSet.as_view(),
            name="project_configuration"),
    re_path(r'^projects/(?P<project_id>[0-9_a-zA-Z\-]+)/config?$', ProjectConfigurationViewSet.as_view(),
            name="project_configuration")
]
