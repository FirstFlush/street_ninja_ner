from enum import Enum


class CustomEnum(Enum):

    @classmethod
    def values(cls):
        return [enum.value for _, enum in cls.__members__.items()]
