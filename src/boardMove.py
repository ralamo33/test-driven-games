from typing import Optional, Tuple
from move import Move
from move_status import MoveStatus
from piece import Piece
from pieceDirection import PieceDirection
from teams import Team


class BoardMove:
    def __init__(self, move: Move, game):
        self.fromRow = move.from_row
        self.fromCol = move.from_col
        self.toRow = move.to_row
        self.toCol = move.to_col
        self.game = game
        self.from_space = self.game.get_space(self.fromRow, self.fromCol)
        self.destination_space = self.game.get_space(self.toRow, self.toCol)

        jump_row = (self.fromRow + self.toRow) // 2
        jump_col = (self.fromCol + self.toCol) // 2
        self.jump_space = self.game.get_space(jump_row, jump_col)

    def handle_move(
        self, active_team: Team, must_double_jump_coordinate: Optional[tuple[int, int]]
    ) -> Tuple[MoveStatus, str]:
        [move_status, explanation] = self.is_valid_with_explanation(
            active_team, must_double_jump_coordinate
        )
        if move_status == MoveStatus.INVALID:
            return move_status, explanation

        piece = self.from_space.get_piece()
        if abs(self.fromCol - self.toCol) == 2:
            return self._handle_jump(piece)

        self._finalize_move(piece)
        return move_status, ""

    def is_valid_with_explanation(
        self, active_team: Team, must_double_jump_coordinate: Optional[tuple[int, int]]
    ) -> Tuple[MoveStatus, str]:
        if self.from_space is None or self.from_space.is_empty():
            return MoveStatus.INVALID, "Invalid space selected"
        if self.destination_space is None:
            return MoveStatus.INVALID, "Destination not on board"
        if must_double_jump_coordinate is not None and must_double_jump_coordinate != (
            self.fromRow,
            self.fromCol,
        ):
            return MoveStatus.INVALID, "Must perform double jump."

        piece = self.from_space.get_piece()

        if not piece.on_team(active_team):
            return MoveStatus.INVALID, "It is not your turn"

        move_direction = (
            PieceDirection.DOWN if self.toRow > self.fromRow else PieceDirection.UP
        )
        if not piece.can_move_in_direction(move_direction):
            return MoveStatus.INVALID, "Wrong direction"

        if not self.destination_space.is_empty():
            return MoveStatus.INVALID, "Destination has another piece"

        if (
            abs(self.fromCol - self.toCol) != abs(self.fromRow - self.toRow)
            or abs(self.fromCol - self.toCol) > 2
        ):
            return MoveStatus.INVALID, "Wrong destination"

        if abs(self.fromCol - self.toCol) == 2:
            if not self._is_valid_jump(piece):
                return MoveStatus.INVALID, "No enemy to jump over"
            return MoveStatus.JUMP, ""

        return MoveStatus.MOVE, ""

    def _handle_jump(self, piece) -> tuple[MoveStatus, str]:
        if not self._is_valid_jump(piece):
            return MoveStatus.INVALID, "No enemy to jump over"
        self.jump_space.delete_piece()
        self._finalize_move(piece)
        if self._has_double_jump():
            return MoveStatus.JUMP_WITH_DOUBLE_JUMP, ""
        return MoveStatus.JUMP, ""

    def _is_valid_jump(self, piece):
        if self.jump_space.is_empty() or not self.destination_space.is_empty():
            return False
        jump_piece = self.jump_space.get_piece()
        return piece.is_enemy(jump_piece)

    def _has_double_jump(self):
        spots_to_check = []
        spots_to_check.append((self.toRow + 2, self.toCol + 2))
        spots_to_check.append((self.toRow + 2, self.toCol - 2))
        spots_to_check.append((self.toRow - 2, self.toCol + 2))
        spots_to_check.append((self.toRow - 2, self.toCol - 2))

        for spot in spots_to_check:
            boardMove = BoardMove(
                Move(
                    from_row=self.toRow,
                    from_col=self.toCol,
                    to_row=spot[0],
                    to_col=spot[1],
                ),
                self.game,
            )
            [move_status, explanation] = boardMove.is_valid_with_explanation(
                self.game.turn, (self.toRow, self.toCol)
                # self.game.turn, self.game.must_double_jump_coordinate
            )
            if move_status == MoveStatus.JUMP:
                return True
        return False

    def _finalize_move(self, piece: Piece):
        self.from_space.delete_piece()
        self.destination_space.add_piece(piece)
        if self.toRow == 0 or self.toRow == 7:
            piece.crown()
