from django.urls import re_path
from users.views.users import UsersViewSet

urlpatterns = [
    re_path(r'', UsersViewSet.as_view(), name="users"),
]
