import logging
import json

from to_do_list_api.exceptions import BaseException
from to_do_list_api.messages import ErrorMessage


logg = logging.getLogger(__name__)


class MissingValueException(BaseException):
    name: str = "MissingValueError"
    logger: logging.Logger = logg

    def __init__(self, message: str) -> None:
        super().__init__(message=message, level=logging.WARNING, exc_info=False)