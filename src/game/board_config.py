from typing import List, Tuple

from game.piece import Piece
from game.piece_direction import PieceDirection
from game.space import Space
from game.team import Team


def create_standard_board() -> List[List[Space]]:
    """Creates a standard 8x8 checkers board with initial piece positions."""
    board = []
    for _ in range(8):
        row = []
        for _ in range(8):
            row.append(Space())
        board.append(row)
    
    # Define starting positions
    white_positions = [
        (0, 1), (0, 3), (0, 5), (0, 7),
        (1, 0), (1, 2), (1, 4), (1, 6),
        (2, 1), (2, 3), (2, 5), (2, 7),
    ]
    
    black_positions = [
        (5, 0), (5, 2), (5, 4), (5, 6),
        (6, 1), (6, 3), (6, 5), (6, 7),
        (7, 0), (7, 2), (7, 4), (7, 6),
    ]
    
    # Place pieces
    for row, col in white_positions:
        board[row][col].add_piece(Piece(direction=PieceDirection.DOWN, team=Team.WHITE))
    
    for row, col in black_positions:
        board[row][col].add_piece(Piece(direction=PieceDirection.UP, team=Team.BLACK))
    
    return board 