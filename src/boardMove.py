from typing import Optional, Tuple
from move import Move
from move_status import MoveStatus
from piece import Piece
from pieceDirection import PieceDirection
from board import Board
from teams import Team


class BoardMove:
    def __init__(self, move: Move, board: Board, active_team: Team, must_double_jump_coordinate: Optional[Tuple[int, int]] = None):
        self.from_row = move.from_row
        self.from_col = move.from_col
        self.to_row = move.to_row
        self.to_col = move.to_col
        self.board = board
        self.active_team = active_team
        self.must_double_jump_coordinate = must_double_jump_coordinate

        self.from_space = self.board.get_space(self.from_row, self.from_col)
        self.destination_space = self.board.get_space(self.to_row, self.to_col)

        jump_row = (self.from_row + self.to_row) // 2
        jump_col = (self.from_col + self.to_col) // 2
        self.jump_space = self.board.get_space(jump_row, jump_col)

    def handle_move(self) -> Tuple[MoveStatus, str]:
        [move_status, explanation] = self.is_valid_with_explanation()
        if move_status == MoveStatus.INVALID:
            return move_status, explanation

        piece = self.from_space.get_piece()
        if abs(self.from_col - self.to_col) == 2:
            return self._handle_jump(piece)

        self._finalize_move(piece)
        return move_status, ""

    def is_valid_with_explanation(self) -> Tuple[MoveStatus, str]:
        if self.from_space is None or self.from_space.is_empty():
            return MoveStatus.INVALID, "Invalid space selected"
        if self.destination_space is None:
            return MoveStatus.INVALID, "Destination not on board"
        if self.must_double_jump_coordinate is not None and self.must_double_jump_coordinate != (
            self.from_row,
            self.from_col,
        ):
            return MoveStatus.INVALID, "Must perform double jump."

        piece = self.from_space.get_piece()

        if not piece.on_team(self.active_team):
            return MoveStatus.INVALID, "It is not your turn"

        move_direction = (
            PieceDirection.DOWN if self.to_row > self.from_row else PieceDirection.UP
        )
        if not piece.can_move_in_direction(move_direction):
            return MoveStatus.INVALID, "Wrong direction"

        if not self.destination_space.is_empty():
            return MoveStatus.INVALID, "Destination has another piece"

        if (
            abs(self.from_col - self.to_col) != abs(self.from_row - self.to_row)
            or abs(self.from_col - self.to_col) > 2
        ):
            return MoveStatus.INVALID, "Wrong destination"

        if abs(self.from_col - self.to_col) == 2:
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
        spots_to_check.append((self.to_row + 2, self.to_col + 2))
        spots_to_check.append((self.to_row + 2, self.to_col - 2))
        spots_to_check.append((self.to_row - 2, self.to_col + 2))
        spots_to_check.append((self.to_row - 2, self.to_col - 2))

        for spot in spots_to_check:
            board_move = BoardMove(
                move=Move(
                    from_row=self.to_row,
                    from_col=self.to_col,
                    to_row=spot[0],
                    to_col=spot[1],
                ),
                board=self.board,
                active_team=self.active_team,
            )
            [move_status, explanation] = board_move.is_valid_with_explanation()
            if move_status == MoveStatus.JUMP:
                return True
        return False

    def _finalize_move(self, piece: Piece):
        self.from_space.delete_piece()
        self.destination_space.add_piece(piece)
        if self.to_row == 0 or self.to_row == 7:
            piece.crown()
