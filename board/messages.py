from typing import List, Union, Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from to_do_list_api.messages import ReturnBaseMessage
from board.constants import TASK_STATUS

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TaskDataMessage:
    title: str
    description: Optional[str] = None
    line_status: Optional[TASK_STATUS] = TASK_STATUS.PENDING

    def __init__(self, **kwargs):
        status = kwargs.get("line_status")
        self.line_status = status if isinstance(status, TASK_STATUS) else TASK_STATUS[status]
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TaskInsertDataMessage(TaskDataMessage):
    def __init__(self, **kwargs): 
        super().__init__(**kwargs)

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class BulkTaskInsertDataMessage:
    tasks: List[TaskDataMessage]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TaskInsertDataReturnMessage(ReturnBaseMessage):
    def __init__(self, consultation_id: str):
        super().__init__(
            type="TaskInsert",
            message="The task was inserted in your board successfully",
            description="Insertion of task in user board",
        )

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class BulkTaskInsertDataReturnMessage(ReturnBaseMessage):
    def __init__(self, consultation_id: str):
        super().__init__(
            type="BulkTaskInsert",
            message="The tasks was inserted in your board successfully",
            description="Insertion of multiples tasks in user board",
        )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class BatchConsultationData:
    ...


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class BatchConsultationReturnMessage(ReturnBaseMessage):
    consultation_id: str
    batch_consultations: List[dict]

    def __init__(self, consultation_id, batch_consultations=[]):
        self.consultation_id = consultation_id
        self.batch_consultations = batch_consultations

        if self.batch_consultations:
            self.message = "success capturing consultation information"
        else:
            self.message = "consultation was not found"

        super().__init__(
            type="BatchConsultation",
            message=self.message,
            description="Get batch's captured information through the consultation_id",
        )