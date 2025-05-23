from game.piece import Piece
from game.piece_direction import PieceDirection
from game.space import Space
from game.team import Team

def test_blank_space():
    space = Space()
    assert space.display() == "_"

def test_white_space(white_piece):
    space = Space()
    space.add_piece(white_piece)
    assert space.display() == "w"

def test_black_space(black_piece):
    space = Space()
    space.add_piece(black_piece)
    assert space.display() == "b"

def test_is_empty():
    space = Space()
    assert space.is_empty()
    space.add_piece(Piece(direction=PieceDirection.DOWN, team=Team.WHITE))
    assert not space.is_empty() 