from typing import List, Tuple, Optional

from game.board import Board
from game.move import Move
from game.team import Team
from game.board_move import BoardMove
from game.move_status import MoveStatus

class PossibleMoves:
    def __init__(self, board: Board):
        self.board = board

    def get_possible_moves(self, active_team: Team, must_double_jump_coordinate: Optional[Tuple[int, int]] = None) -> List[Move]:
        moves: List[Move] = []
        for from_row, row in enumerate(self.board.board):
            for from_col, space in enumerate(row):
                if space.is_empty():
                    continue
                piece = space.get_piece()
                if not piece.on_team(active_team):
                    continue
                    
                if must_double_jump_coordinate and (from_row, from_col) != must_double_jump_coordinate:
                    continue
                    
                destinations = self._get_possible_destinations(from_row, from_col)
                for destination in destinations:
                    (to_row, to_col) = destination
                    board_move = BoardMove(
                        move=Move(
                            from_row=from_row,
                            from_col=from_col,
                            to_row=to_row,
                            to_col=to_col,
                        ),
                        board=self.board,
                        active_team=active_team,
                        must_double_jump_coordinate=must_double_jump_coordinate
                    )
                    [move_status, explanation] = board_move.is_valid_with_explanation()
                    
                    if move_status != MoveStatus.INVALID:
                        moves.append(
                            Move(
                                from_row=from_row,
                                from_col=from_col,
                                to_row=to_row,
                                to_col=to_col,
                            )
                        )
        return moves

    def _get_possible_destinations(self, row: int, col: int) -> List[Tuple[int, int]]:
        standard_destinations = [
            (row + 1, col + 1),
            (row + 1, col + -1),
            (row + -1, col + 1),
            (row + -1, col + -1),
        ]
        jump_destinations = [
            (row + 2, col + 2),
            (row + 2, col + -2),
            (row + -2, col + 2),
            (row + -2, col + -2),
        ]
        return standard_destinations + jump_destinations 