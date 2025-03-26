from typing import Optional
from pydantic.dataclasses import dataclass
from game.move_status import MoveStatus
from game.piece_direction import PieceDirection
from game.space import Space
from game.team import Team


@dataclass
class Move:
    from_row: int
    from_col: int
    to_row: int
    to_col: int
