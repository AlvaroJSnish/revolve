from django.urls import path, include

urlpatterns = [
    path('', include(('projects.urls.project',
         'projects'), namespace="projects")),
]
