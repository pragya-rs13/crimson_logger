from enum import Enum

_ORDINAL_MAP = {"DEBUG": 10, "INFO": 20, "WARN": 30, "ERROR": 40, "FATAL": 50}


class LogLevel(str, Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"

    def __lt__(self, other):
        if isinstance(other, LogLevel):
            return _ORDINAL_MAP[self.value] < _ORDINAL_MAP[other.value]
        return NotImplemented

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other
