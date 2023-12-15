from drf_spectacular.utils import OpenApiParameter, OpenApiExample, OpenApiResponse, OpenApiRequest

from .models import TaskStatus


class BoardManagerGetSchema:
    description = 'Get tasks of the authenticated user. If you do not pass \
        any parameters, only pending tasks will be returned '
    
    parameters = [
        OpenApiParameter(
            name='title',
            description='matches exact title',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='title__icontains',
            description='matches the title containing the text\
                  (case insensitive)',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='description',
            description='matches exact description',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='description__icontains',
            description='matches task status',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='status',
            description='matches task status',
            required=False,
            type=str,
            enum=TaskStatus._member_map_
        ),
    ]

    examples = [
        OpenApiExample(
            name='Get all pending tasks of the authenticated user',
            description='Get all pending tasks from authenticated user \
                when no parameters are specified',
            value=[
                {
                    "id": "45214d30-a875-4127-beea-68f7256db287",
                    "title": "Wash the car",
                    "description": "Don't forget to polish",
                    "status": "PENDING",
                    "statusLabel": "The task is pending",
                    "createdAt": "2023-12-14T08:35:14.579391Z",
                    "updatedAt": "2023-12-14T08:54:10.061857Z"
                },
                {
                    "id": "0d015c25-47bd-4200-a8dc-9cb150b321ba",
                    "title": "Organize the books",
                    "description": None,
                    "status": "PENDING",
                    "statusLabel": "The task is pending",
                    "createdAt": "2023-12-14T08:35:14.579343Z",
                    "updatedAt": None
                }
            ]
        ),
        OpenApiExample(
            name='Get specific tasks tasks of the authenticated user',
            description='Get specific tasks from authenticated user \
                when use parameters',
            value=[
                {
                    "id": "45214d30-a875-4127-beea-68f7256db287",
                    "title": "Wash the car",
                    "description": "Don't forget to polish",
                    "status": "CONCLUDED",
                    "statusLabel": "The task is pending",
                    "createdAt": "2023-12-14T08:35:14.579391Z",
                    "updatedAt": "2023-12-14T08:54:10.061857Z"
                },
                {
                    "id": "0d015c25-47bd-4200-a8dc-9cb150b321ba",
                    "title": "Organize the books",
                    "description": None,
                    "status": "CONCLUDED",
                    "statusLabel": "The task is pending",
                    "createdAt": "2023-12-14T08:35:14.579343Z",
                    "updatedAt": "2023-12-14T08:54:10.061857Z"
                }
            ]
        ),
    ]


class BoardManagerPostSchema:
    description = 'Create task for the authenticated user. You can use it to \
        create just one task or multiple ones, it just depends on whether you \
        use dict or array in the request body. The tasks will be created as \
        pending if the status is not specified'
    
    response_examples = [
        OpenApiExample(
            name='Bulk Insertion of tasks',
            description='Insertion of multiples tasks in user board',
            value=[
                {
                    "type": "BulkTaskInsert",
                    "message": '''The tasks was inserted in your board '''
                     '''successfully''',
                    "description": "Insertion of multiples tasks in user board"
                }
            ]
        ),
        OpenApiExample(
            name='Insertion of tasks',
            description='Insertion of a tasks in user board',
            value=[
                {
                    "type": "TaskInsert",
                    "message": '''The task was inserted in your board '''
                     '''successfully''',
                    "description": "Insertion of a tasks in user board"
                }
            ]
        )
    ]

    request_examples = [
        OpenApiExample(
            name='Bulk Insertion of tasks',
            description='Insertion of multiples tasks in user board',
            value=[
                    {
                        "title": "Wash the car"
                    },
                    {
                        "title": "Organize the books",
                        'status': 'concluded'
                    },
                    {
                        "title": "Cook lunch for the family",
                        "description": "Don't make chicken!!"
                    },
            ]
        ),
        OpenApiExample(
            name='Insertion of tasks',
            description='Insertion of a tasks in user board',
            value={
                "title": "Water the plants",
            }
        )
    ]

    responses=OpenApiResponse(
        response={''},
        description='',
        examples=response_examples,
    )

    request = OpenApiRequest(
        request='',
        encoding={},
        examples=request_examples
    )


class BoardManagerPutSchema:
    description = 'Update task for the authenticated user. You can use it to \
        update just one task or multiple ones, it just depends on whether you \
        use dict or array in the request body. The tasks will be updated for \
        concluded if the status is not specified'
    
    response_examples = [
        OpenApiExample(
            name='Bulk Update of tasks',
            description='Multiple tasks update in user board',
            value=[
                {
                    "type": "BulkTaskUpdate",
                    "message": '''The tasks was updated successfully''',
                    "description": "Multiple tasks update in user board"
                }
            ]
        ),
        OpenApiExample(
            name='Update of a task',
            description='Updating of a task in user board',
            value=[
                {
                    "type": "TaskUpdate",
                    "message": '''The task was updated successfully''',
                    "description": "Updating of a task in user board"
                }
            ]
        )
    ]

    request_examples = [
        OpenApiExample(
            name='Bulk Update of tasks',
            description='Multiple tasks update status',
            value=[
                {
                    "task": "89392d02-190a-4d72-b91e-0312d9a379bc",
                },
                {
                    "task": "45214d30-a875-4127-beea-68f7256db287",
                    "status": "Pending" 
                },
                {
                    "task": "c2370bd8-e526-4672-978c-040b762ecb8d",
                    "status": "Canceled"
                }
            ]
        ),
        OpenApiExample(
            name='Update a task',
            description='Updating status of the task to through task_id \
                parameter',
            value={
                "status": "pending"
            }
        )
    ]

    responses=OpenApiResponse(
        response={''},
        description='',
        examples=response_examples,
    )

    request = OpenApiRequest(
        request='',
        encoding={},
        examples=request_examples
    )

class BoardManagerDeleteSchema:
    description = 'Cancel task for the authenticated user. You can use it to \
        cancel just one task or multiple ones, it just depends on whether you \
        use dict or array in the request body'

    parameters = [
        OpenApiParameter(
            name='task_id',
            description='set the id of a task',
            required=False,
            type=str
        ),
    ]

    response_examples = [
        OpenApiExample(
            name='Cancelation of a task',
            description='Cancelation of a task in user board',
            value=[
                {
                    "type": "TaskCancel",
                    "message": 'The task was canceled successfully',
                    "description": "Task cancelation in user board"
                }
            ]
        ),
        OpenApiExample(
            name='Bulk Cancelation of tasks',
            description='Multiple tasks cancelation in user board',
            value=[
                {
                    "type": "BulkTaskCancel",
                    "message": 'The tasks was canceled successfully',
                    "description": "Multiple tasks cancelation in user board"
                }
            ]
        ),
    ]

    responses=OpenApiResponse(
        response={'a':'1'},
        description='',
        examples=response_examples,
    )