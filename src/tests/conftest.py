import pytest
from game import Game
from move import Move
from piece import Piece
from pieceDirection import PieceDirection
from teams import Team

@pytest.fixture
def game():
    return Game()

@pytest.fixture
def white_piece():
    return Piece(direction=PieceDirection.DOWN, team=Team.WHITE)

@pytest.fixture
def black_piece():
    return Piece(direction=PieceDirection.UP, team=Team.BLACK)

@pytest.fixture
def crowned_game():
    game = Game()
    # Setup moves to get a crowned piece
    moves = [
        (2, 1, 3, 0), (5, 0, 4, 1),
        (2, 3, 3, 2), (5, 2, 4, 3),
        (1, 2, 2, 3), (4, 3, 2, 1),
        (1, 0, 3, 2), (3, 2, 5, 0),
        (5, 4, 4, 3), (0, 1, 1, 2),
        (4, 3, 3, 2), (2, 3, 3, 4),
        (3, 2, 2, 1), (2, 5, 3, 6),
        (2, 1, 1, 0), (3, 6, 4, 7),
        (1, 0, 0, 1)
    ]
    for from_row, from_col, to_row, to_col in moves:
        game.move(Move(from_row, from_col, to_row, to_col))
    return game 