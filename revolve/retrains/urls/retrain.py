from django.urls import re_path

from retrains.views import RetrainView

urlpatterns = [
    re_path(r'^retrain/(?P<project_id>[0-9_a-zA-Z\-]+)?$', RetrainView.as_view(), name="retrain"),
]
