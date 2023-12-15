import json

from django.conf import settings
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from dacite.exceptions import MissingValueError
from dacite import from_dict
from dataclasses import asdict

from .messages import (
    TaskInsertDataMessage,
    TaskInsertDataReturnMessage,
    BulkTaskInsertDataReturnMessage,
    TaskFilterParamsDataMessage,
    TaskUpdateParamsDataMessage,
    TaskUpdateDataReturnMessage,
    BulkTaskUpdateDataReturnMessage,
    TaskCancelParamsDataMessage,
    TaskCancelDataReturnMessage,
    BulkTaskCancelDataReturnMessage,
)
from .exceptions import (
    BaseException,
    MissingValueException,
    StatusDoesNotExistException,
    TaskDoesNotExistException,
)
from .serializers import UserTasksSerializer
from .models import Task, TaskStatus

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def cleanup_user_task_filter(params: dict) -> dict:
    filter = {}
    for param in params:
        params[param] and filter.update({param:params[param]})
    return filter
          

class BoardManager(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        try:
            try:
                if isinstance(request.data, dict):
                    new_task = from_dict(TaskInsertDataMessage, request.data)
                    
                    with transaction.atomic():
                        Task.objects.create(
                            user=request.user,
                            **new_task.to_dict()  
                        )

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
                        Task.objects.bulk_create(bulk_tasks)

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
        
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, **kwargs):
        try:
            task_id = kwargs.get('task_id')
            if task_id:
                try:
                    user_tasks = [Task.objects.get(
                        id=task_id, user=request.user
                    )]
                except Task.DoesNotExist as e:
                    message = TaskDoesNotExistException(task_id).message
                    return Response(
                        message, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                try:
                    data = (request.query_params 
                            if hasattr(request, 'query_params') else dict()
                    )
                    params = from_dict(
                        TaskFilterParamsDataMessage, data
                    )
                    filters = cleanup_user_task_filter(asdict(params))
                    user_tasks = request.user.tasks.filter(**filters)
                except StatusDoesNotExistException as e:
                    return Response(
                        e.message, status=status.HTTP_400_BAD_REQUEST
                    )

            user_tasks_serialized = UserTasksSerializer(user_tasks, many=True)
            return Response(
                user_tasks_serialized.data, status=status.HTTP_200_OK
            )
                
        except Exception as e:
                return Response(
                    BaseException(str(e)).message,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

    def put(self, request, **kwargs):
        try:
            try:
                request_data = request.data if hasattr(request, 'data') else {}
                if isinstance(request_data, dict):
                    task_id = kwargs.get('task_id')
                    try:
                        update_task = from_dict(
                            TaskUpdateParamsDataMessage, {'task': task_id, 
                                'user': request.user,
                                **request_data,
                            }
                        )
                    except Task.DoesNotExist as e:
                        message = TaskDoesNotExistException(task_id).message
                        return Response(
                            message, status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    with transaction.atomic():
                        update_task.task.update_status(update_task.status)

                    return Response(
                        json.loads(TaskUpdateDataReturnMessage().to_json()),
                        status=status.HTTP_200_OK
                    )

                elif isinstance(request.data, list):
                    update_tasks = []
                    for task in request.data:
                        task['user'] = request.user
                        new_params = from_dict(
                            TaskUpdateParamsDataMessage, task
                        )
                        update_tasks.append(new_params)

                    update_task: TaskUpdateParamsDataMessage
                    with transaction.atomic():
                        for update_task in update_tasks:
                            update_task.task.update_status(update_task.status)

                    return Response(
                        json.loads(BulkTaskUpdateDataReturnMessage().to_json()),
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

    def delete(self, request, **kwargs):
        try:
            try:
                request_data = request.data if hasattr(request, 'data') else {}
                if isinstance(request_data, dict):
                    task_id = kwargs.get('task_id')
                    try:
                        cancel_task = from_dict(
                            TaskCancelParamsDataMessage, 
                            {'task': task_id, 'user': request.user}
                        )
                    except Task.DoesNotExist as e:
                        message = TaskDoesNotExistException(task_id).message
                        return Response(
                            message, status=status.HTTP_400_BAD_REQUEST
                        )

                    with transaction.atomic():
                        cancel_task.task.update_status(TaskStatus.CANCELED)

                    return Response(
                        json.loads(TaskCancelDataReturnMessage().to_json()),
                        status=status.HTTP_200_OK
                    )

                elif isinstance(request.data, list):
                    update_tasks = []
                    for task_id in request.data:
                        new_params = from_dict(
                            TaskUpdateParamsDataMessage,
                            {'task': task_id, 'user': request.user}
                        )
                        update_tasks.append(new_params)

                    update_task: TaskUpdateParamsDataMessage
                    with transaction.atomic():
                        for update_task in update_tasks:
                            update_task.task.update_status(TaskStatus.CANCELED)

                    return Response(
                        json.loads(BulkTaskCancelDataReturnMessage().to_json()),
                        status=status.HTTP_200_OK
                    )

            except MissingValueError as e:
                message = MissingValueException(str(e)).message
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
                return Response(
                    BaseException(str(e)).message,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
