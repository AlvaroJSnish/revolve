from django.urls import re_path
from users.views.auth import SignInView, SignOutView

urlpatterns = [
    re_path(r'^signin/?$', SignInView.as_view(), name="signin"),
    re_path(r'^signout/?$', SignOutView.as_view(), name="signout"),
]
