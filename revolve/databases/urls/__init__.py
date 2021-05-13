from django.urls import path, include

urlpatterns = [
    path('', include(('databases.urls.database',
                      'databases'), namespace="databases")),
]
