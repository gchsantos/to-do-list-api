from uuid import UUID
from typing import Optional, Union

from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from django.contrib.auth.models import User

from to_do_list_api.messages import ReturnBaseMessage
from .models import TaskStatus, Task
from .exceptions import StatusDoesNotExistException

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TaskInsertDataMessage:
    title: str
    description: Optional[str]
    status: Optional[str] = TaskStatus.PENDING
    
    def __init__(self, **kwargs):
        status = kwargs.get("status")
        if isinstance(status, TaskStatus):
            self.status = status
        else:
            try:
                self.status = TaskStatus.get_status_by_name(status)
            except KeyError as status:
                raise StatusDoesNotExistException(status)
            
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TaskInsertDataReturnMessage(ReturnBaseMessage):
    def __init__(self):
        super().__init__(
            type="TaskInsert",
            message="The task was inserted in your board successfully",
            description="Insertion of task in user board",
        )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TaskUpdateDataReturnMessage(ReturnBaseMessage):
    def __init__(self):
        super().__init__(
            type="TaskUpdate",
            message="The task was updated successfully",
            description="Updating of a task in user board",
        )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class BulkTaskInsertDataReturnMessage(ReturnBaseMessage):
    def __init__(self):
        super().__init__(
            type="BulkTaskInsert",
            message="The tasks was inserted in your board successfully",
            description="Insertion of multiples tasks in user board",
        )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TaskCancelDataReturnMessage(ReturnBaseMessage):
    def __init__(self):
        super().__init__(
            type="TaskCancel",
            message="The task was canceled successfully",
            description="Task cancelation in user board",
        )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class BulkTaskCancelDataReturnMessage(ReturnBaseMessage):
    def __init__(self):
        super().__init__(
            type="BulkTaskCancel",
            message="The tasks was canceled successfully",
            description="Multiple tasks cancelation in user board",
        )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class BulkTaskUpdateDataReturnMessage(ReturnBaseMessage):
    def __init__(self):
        super().__init__(
            type="BulkTaskUpdate",
            message="The tasks was updated successfully",
            description="Multiple tasks update in user board",
        )


@dataclass
class TaskFilterParamsDataMessage:
    title: Optional[str]
    description: Optional[str]
    title__icontains: Optional[str]
    description__icontains: Optional[str]
    status: Optional[str] = TaskStatus.PENDING
    
    def __init__(self, **kwargs):
        status = kwargs.get("status")
        if isinstance(status, TaskStatus):
            self.status = status
        else:
            try:
                self.status = TaskStatus.get_status_by_name(status).value
            except KeyError as status:
                raise StatusDoesNotExistException(status)
            
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.title__icontains = kwargs.get('title__icontains')
        self.description__icontains = kwargs.get('description__icontains')


@dataclass
class TaskUpdateParamsDataMessage:
    user: User
    task: Optional[Union[str, Task]]
    status: Optional[str] = TaskStatus.CONCLUDED
    
    def __init__(self, **kwargs):
        status = kwargs.get("status")
        task = kwargs.get("task")
        user = kwargs.get("user")

        if isinstance(status, TaskStatus):
            self.status = status
        else:
            try:
                self.status = TaskStatus.get_status_by_name(status).value
            except KeyError as status:
                raise StatusDoesNotExistException(status)
            
        if task and UUID(task):   
            self.task = Task.objects.get(id=kwargs.get("task"), user=user)


@dataclass
class TaskCancelParamsDataMessage:
    user: User
    task: Optional[Union[str, Task]]
    
    def __init__(self, **kwargs):
        task = kwargs.get("task")
        user = kwargs.get("user")
        
        if task and UUID(task):   
            self.task = Task.objects.get(id=kwargs.get("task"), user=user)
