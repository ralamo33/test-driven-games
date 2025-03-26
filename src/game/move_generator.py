from typing import List, Tuple

from game.board import Board
from game.move import Move
from game.teams import Team
from game.boardMove import BoardMove
from move_status import MoveStatus

class MoveGenerator:
    def __init__(self, board: Board):
        self.board = board

    def get_possible_moves(self, active_team: Team) -> List[Move]:
        moves: List[Move] = []
        for from_row, row in enumerate(self.board.board):
            for from_col, space in enumerate(row):
                if space.is_empty():
                    continue
                piece = space.get_piece()
                if not piece.on_team(active_team):
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