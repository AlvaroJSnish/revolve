from django.urls import path, include

urlpatterns = [
    path('', include(('retrains.urls.retrain',
                      'retrains'), namespace="retrains")),
]
