import pytest
from move import Move

def test_down_valid(game):
    moving_piece = game._get_space(2, 1).piece
    game.move(Move(from_row=2, from_col=1, to_row=3, to_col=0))
    piece_in_new_space = game._get_space(3, 0).piece
    assert moving_piece == piece_in_new_space
    original_space = game._get_space(2, 1)
    assert original_space.piece is None

def test_negative_row(game):
    with pytest.raises(ValueError):
        game.move(Move(from_row=2, from_col=1, to_row=-1, to_col=0))

def test_negative_col(game):
    with pytest.raises(ValueError):
        game.move(Move(from_row=2, from_col=1, to_row=3, to_col=-1))

def test_wrong_direction(game):
    game.move(Move(from_row=2, from_col=1, to_row=3, to_col=0))
    with pytest.raises(ValueError):
        game.move(Move(from_row=3, from_col=0, to_row=2, to_col=1))

    game.move(Move(5, 0, 4, 1))
    with pytest.raises(ValueError):
        game.move(Move(4, 1, 5, 0))

def test_destination_over_board(game):
    with pytest.raises(ValueError):
        game.move(Move(from_row=2, from_col=7, to_row=3, to_col=8))

def test_invalid_move_on_board(game):
    from_row = 2
    from_col = 1
    side_length = 8
    for to_row in range(side_length):
        for to_col in range(side_length):
            if to_row == 3 and to_col in [0, 2]:
                continue
            with pytest.raises(ValueError):
                game.move(Move(from_row, from_col, to_row, to_col))

def test_destination_has_another_piece(game):
    with pytest.raises(ValueError, match="Destination has another piece"):
        game.move(Move(0, 1, 1, 0))

def test_eat_enemy(game):
    # Setup the board for eating
    game.move(Move(2, 1, 3, 0))
    game.move(Move(5, 0, 4, 1))
    game.move(Move(2, 3, 3, 2))
    game.move(Move(5, 2, 4, 3))
    game.move(Move(1, 2, 2, 3))

    original_piece = game._get_space(4, 3).piece
    game.move(Move(4, 3, 2, 1))
    assert game._get_space(2, 1).piece == original_piece
    assert game._get_space(3, 2).piece is None
    assert game._get_space(4, 3).piece is None
    game.move(Move(2, 3, 3, 4))

def test_cannot_eat_if_destination_filled(game):
    # Setup the board
    game.move(Move(2, 1, 3, 0))
    game.move(Move(5, 0, 4, 1))
    game.move(Move(2, 3, 3, 2))
    game.move(Move(5, 2, 4, 3))
    game.move(Move(1, 0, 2, 1))
    game.move(Move(5, 6, 4, 7))

    with pytest.raises(ValueError, match="Destination has another piece"):
        game.move(Move(3, 2, 5, 4))

def test_cannot_eat_friend(game):
    game.move(Move(2, 1, 3, 0))
    game.move(Move(5, 0, 4, 1))
    game.move(Move(2, 3, 3, 2))
    game.move(Move(5, 2, 4, 3))
    game.move(Move(1, 0, 2, 1))
    with pytest.raises(ValueError, match="No enemy to jump over"):
        game.move(Move(6, 7, 4, 5))

def test_player_cannot_go_twice(game):
    game.move(Move(2, 1, 3, 0))
    with pytest.raises(ValueError, match="It is not your turn"):
        game.move(Move(3, 0, 4, 1)) 