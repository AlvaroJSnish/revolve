from re import sub

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from projects.models import Project, ProjectConfiguration
from retrains.models import Retrain
from retrains.serializers import RetrainCreateSerializer
from retrains.tasks import retrain_basic_regression_model


class RetrainView(CreateAPIView):
    serializer_class = RetrainCreateSerializer

    def post(self, request, *args, **kwargs):
        result_status = status.HTTP_201_CREATED
        result_dict = {}

        auth = authenticate(request)

        if auth:
            from_database = self.request.data['from_database']
            project_id = self.kwargs.get('project_id')

            if from_database:
                project = Project.objects.get(id=project_id)
                project_config = ProjectConfiguration.objects.get(project=project)
                request.data['database'] = str(project_config.database.id)
                request.data['project'] = project_id

                serializer = self.get_serializer(data=request.data)

                if not serializer.is_valid():
                    result_status = status.HTTP_400_BAD_REQUEST
                    result_dict["reasons"] = serializer.errors
                else:
                    retrain_s = serializer.save()

                    token = sub('Token ', '', self.request.META.get(
                        'HTTP_AUTHORIZATION', None))

                    task = retrain_basic_regression_model.apply_async(args=[request.data, str(project.id), token])

                    retrain = Retrain.objects.get(id=retrain_s.id)

                    retrain.task_id = task.id
                    retrain.save(force_update=True)

                    result_dict = RetrainCreateSerializer(retrain).data

        else:
            result_status = status.HTTP_401_UNAUTHORIZED
            result_status["reasons"] = 'Not authorized'

        return Response(result_dict, status=result_status)
