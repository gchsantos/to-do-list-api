from typing import Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from to_do_list_api.messages import ReturnBaseMessage
from .models import TaskStatus
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
class BulkTaskInsertDataReturnMessage(ReturnBaseMessage):
    def __init__(self):
        super().__init__(
            type="BulkTaskInsert",
            message="The tasks was inserted in your board successfully",
            description="Insertion of multiples tasks in user board",
        )
