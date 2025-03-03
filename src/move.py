from typing import Optional
from pydantic.dataclasses import dataclass
from move_status import MoveStatus
from pieceDirection import PieceDirection
from space import Space
from teams import Team


@dataclass
class Move:
    from_row: int
    from_col: int
    to_row: int
    to_col: int


@dataclass
class PotentialMove:
    from_row: int
    from_col: int
    from_space: Optional[Space]
    to_row: int
    to_col: int
    to_space: Optional[Space]
    jump_space: Optional[Space]

    def is_valid_with_explanation(
        self, active_team: Team, must_double_jump_coordinate: Optional[tuple[int, int]]
    ) -> tuple[MoveStatus, str]:
        if self.from_space is None or self.from_space.is_empty():
            return (MoveStatus.INVALID, "Invalid space selected")
        if self.to_space is None:
            return (MoveStatus.INVALID, "Destination not on board")
        if must_double_jump_coordinate is not None and must_double_jump_coordinate != (
            self.from_row,
            self.from_col,
        ):
            return (MoveStatus.INVALID, "Must perform double jump.")

        piece = self.from_space.get_piece()

        if not piece.on_team(active_team):
            return (MoveStatus.INVALID, "It is not your turn")

        move_direction = (
            PieceDirection.DOWN if self.to_row > self.from_row else PieceDirection.UP
        )
        if not piece.can_move_in_direction(move_direction):
            return (MoveStatus.INVALID, "Wrong direction")

        if not self.to_space.is_empty():
            return (MoveStatus.INVALID, "Destination has another piece")

        if (
            abs(self.from_col - self.to_col) != abs(self.from_row - self.to_row)
            or abs(self.from_col - self.to_col) > 2
        ):
            return (MoveStatus.INVALID, "Wrong destination")

        if abs(self.from_col - self.to_col) == 2:
            if not self._is_valid_jump(piece):
                return (MoveStatus.INVALID, "No enemy to jump over")
            return (MoveStatus.JUMP, "")

        return (MoveStatus.MOVE, "")

    def _is_valid_jump(self, piece):
        if self.jump_space.is_empty() or not self.to_space.is_empty():
            return False
        jump_piece = self.jump_space.get_piece()
        return piece.is_enemy(jump_piece)
