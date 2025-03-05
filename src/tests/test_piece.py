from pieceDirection import PieceDirection
from teams import Team

def test_piece_direction(white_piece):
    assert white_piece.can_move_in_direction(PieceDirection.DOWN)
    assert not white_piece.can_move_in_direction(PieceDirection.UP)

def test_piece_team(white_piece, black_piece):
    assert white_piece.on_team(Team.WHITE)
    assert not white_piece.on_team(Team.BLACK)

def test_piece_against_team(white_piece, black_piece):
    assert white_piece.against_team(Team.BLACK)
    assert not white_piece.against_team(Team.WHITE)

def test_piece_is_enemy(white_piece, black_piece):
    assert white_piece.is_enemy(black_piece)
    assert not white_piece.is_enemy(white_piece)

def test_direction_is_valid():
    assert PieceDirection.UP.is_valid_direction(PieceDirection.UP)
    assert PieceDirection.DOWN.is_valid_direction(PieceDirection.DOWN)
    assert PieceDirection.BOTH.is_valid_direction(PieceDirection.UP)
    assert PieceDirection.BOTH.is_valid_direction(PieceDirection.DOWN) 