from typing import Optional
from pydantic.dataclasses import dataclass
from move_status import MoveStatus
from game.pieceDirection import PieceDirection
from game.space import Space
from game.teams import Team


@dataclass
class Move:
    from_row: int
    from_col: int
    to_row: int
    to_col: int
