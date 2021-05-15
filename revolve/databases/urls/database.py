from django.urls import re_path

from databases.views import DatabasesViewSet, DatabaseConnect, CheckDbConnection

urlpatterns = [
    re_path(r'^databases/?$', DatabasesViewSet.as_view(), name="databases"),
    re_path(r'^databases/check-connection/?$', CheckDbConnection.as_view(), name="database_check_connection"),
    re_path(r'^databases/(?P<database_id>[0-9_a-zA-Z\-]+)?$', DatabaseConnect.as_view(),
            name="database_connect"),
]
