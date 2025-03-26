from enum import Enum


class MoveStatus(Enum):
    INVALID = "INVALID"
    MOVE = "MOVE"
    JUMP = "JUMP"
    JUMP_WITH_DOUBLE_JUMP = "JUMP_WITH_DOUBLE_JUMP"
