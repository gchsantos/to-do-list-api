import logging

from to_do_list_api.exceptions import BaseException


logg = logging.getLogger(__name__)


class MissingValueException(BaseException):
    name: str = "MissingValueError"
    logger: logging.Logger = logg

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message, level=logging.WARNING, exc_info=False
        )


class StatusDoesNotExistException(BaseException):
    name: str = "StatusDoesNotExistError"
    logger: logging.Logger = logg

    def __init__(self, status: str) -> None:
        message = f"The status '{status}' is invalid"
        super().__init__(
            message=message, level=logging.WARNING, exc_info=False
        )

class TaskDoesNotExistException(BaseException):
    name: str = "TaskDoesNotExistError"
    logger: logging.Logger = logg

    def __init__(self, task_id: str) -> None:
        message = f"The task id '{task_id}' not exists"
        super().__init__(
            message=message, level=logging.WARNING, exc_info=False
        )
