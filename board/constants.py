from enum import IntEnum


class LINE_STATUS(IntEnum):
    PENDING = 1
    CONCLUDED = 2
    CANCELLED = 3

    @classmethod
    def get_status(cls):
        return [(key.value, key.name) for key in cls]