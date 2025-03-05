from move import Move
from pieceDirection import PieceDirection
from teams import Team

def test_crown_piece(crowned_game):
    crowned_space = crowned_game._get_space(0, 1)
    crowned_piece = crowned_space.piece
    assert crowned_piece.direction == PieceDirection.BOTH
    assert crowned_space.display() == "B"

def test_triple_jump_with_crown(crowned_game):
    crowned_game.move(move=Move(2, 7, 3, 6))
    crowned_game.move(move=Move(0, 1, 2, 3))
    crowned_game.move(move=Move(2, 3, 4, 5))
    assert crowned_game.turn == Team.BLACK
    crowned_game.move(move=Move(4, 5, 2, 7)) 