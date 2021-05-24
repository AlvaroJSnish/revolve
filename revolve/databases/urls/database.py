from django.urls import re_path

from databases.views import DatabasesViewSet, CheckDbConnection, DatabaseViewSet, DatabaseTables, DatabaseGetTable, \
    DatabasesLite

urlpatterns = [
    re_path(r'^databases/?$', DatabasesViewSet.as_view(), name="databases"),
    re_path(r'^databases-lite/?$', DatabasesLite.as_view(), name="databases-lite"),
    re_path(r'^databases/check-connection/?$', CheckDbConnection.as_view(), name="database_check_connection"),
    re_path(r'^databases/(?P<database_id>[0-9_a-zA-Z\-]+)?$', DatabaseViewSet.as_view(),
            name="database_connect"),
    re_path(r'^databases/(?P<database_id>[0-9_a-zA-Z\-]+)/tables?$', DatabaseTables.as_view(),
            name="database_get_tables"),
    re_path(r'^databases/(?P<database_id>[0-9_a-zA-Z\-]+)/tables/(?P<table_name>[0-9_a-zA-Z\-]+)?$',
            DatabaseGetTable.as_view(),
            name="database_get_table"),
]
