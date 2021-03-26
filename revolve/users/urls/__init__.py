from django.urls import path, include

urlpatterns = [
    path('auth/', include(('users.urls.auth', 'users'), namespace="auth")),
    path('users/', include(('users.urls.user', 'users'), namespace="users")),
]
