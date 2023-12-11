import json
from typing import List, Dict

from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from dacite.exceptions import MissingValueError

from .messages import TaskInsertDataMessage, BulkTaskInsertDataMessage, TaskDataMessage
from .exceptions import (
    BaseException,
    MissingValueException,
)
from .models import Task

class BoardManager(APIView):
    permission_classes = []

    def post(self, request, **kwargs):
        try:
            try:
                if isinstance(request.data, dict):
                    insert_message = TaskDataMessage.from_json(json.dumps(request.data))
                elif isinstance(request.data, list):
                    insert_message = BulkTaskInsertDataMessage(request.data)
                    
                print(insert_message)
            except MissingValueError as e:
                return Response(
                    MissingValueException(str(e)).message,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # generator_cnjs: Dict[str, List[BatchLine]] = dict()

            # for cnj in insert_message.cnjs:
            #     try:
            #         uf = get_uf_by_cnj(cnj)
            #         if not uf:
            #             raise UnsupportedCNJException(cnj)

            #         generator_cnjs.setdefault(uf, []).append(BatchLine(cnj=cnj, uf=uf))
            #     except (UnsupportedCNJException, ValueError) as e:
            #         message = (
            #             e.message
            #             if hasattr(e, "message")
            #             else UnsupportedCNJException(cnj).message
            #         )
            #         return Response(
            #             message,
            #             status=status.HTTP_400_BAD_REQUEST,
            #         )

            # with transaction.atomic():
            #     generator = BatchGenerator.objects.create(
            #         refresh_lawsuit=insert_message.refresh_lawsuit,
            #         user=request.user,
            #     )
            #     generator.generate(generator_cnjs, insert_message.public_consultation)

            # return_message = json.loads(
            #     BatchInsertDataReturnMessage(generator.consultation.id).to_json()
            # )
            return Response(json.loads(insert_message.to_json()), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                BaseException(str(e)).message,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )