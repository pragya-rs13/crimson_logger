from enum import Enum


class WriteMode(str, Enum):
    SYNC = "SYNC"
    ASYNC = "ASYNC"
