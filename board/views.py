import json

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from dacite.exceptions import MissingValueError
from dacite import from_dict

from .messages import (
    TaskInsertDataMessage,
    TaskInsertDataReturnMessage,
    BulkTaskInsertDataReturnMessage,
)
from .exceptions import (
    BaseException,
    MissingValueException,
    StatusDoesNotExistException,
)
from .models import Task

class BoardManager(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        try:
            try:
                if isinstance(request.data, dict):
                    new_task = from_dict(TaskInsertDataMessage, request.data)
                    
                    with transaction.atomic():
                        print(Task.objects.create(
                            user=request.user,
                            **new_task.to_dict()  
                        ))

                    return Response(
                        json.loads(TaskInsertDataReturnMessage().to_json()),
                        status=status.HTTP_200_OK
                    )

                elif isinstance(request.data, list):
                    new_tasks = []
                    for task in request.data:
                        data_task = from_dict(TaskInsertDataMessage, task)
                        new_tasks.append(data_task)

                    bulk_tasks = []
                    with transaction.atomic():
                        for task in new_tasks:
                            bulk_tasks.append(Task(
                                user=request.user,
                                **task.to_dict()
                            ))
                        print(Task.objects.bulk_create(bulk_tasks))

                    return Response(
                        json.loads(BulkTaskInsertDataReturnMessage().to_json()),
                        status=status.HTTP_200_OK
                    )

            except MissingValueError as e:
                message = MissingValueException(str(e)).message
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            except StatusDoesNotExistException as e:
                return Response(e.message, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                BaseException(str(e)).message,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )