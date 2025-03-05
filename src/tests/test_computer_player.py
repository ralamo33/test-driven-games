from move import Move
from teams import Team

def test_get_starting_moves(game):
    moves = game._get_possible_moves()
    assert len(moves) == 7
    assert Move(2, 1, 3, 0) in moves

def test_advanced_moves(game):
    game.move(Move(2, 1, 3, 0))
    game.move(Move(5, 0, 4, 1))
    game.move(Move(2, 3, 3, 2))
    game.move(Move(5, 2, 4, 3))
    game.move(Move(1, 2, 2, 3))
    moves = game._get_possible_moves()
    assert len(moves) == 8

def test_computer_player(game):
    game._computer_move()
    movable_cords = [(2, 1), (2, 3), (2, 5), (2, 7)]
    made_move = False
    for cord in movable_cords:
        space = game.board.get_space(cord[0], cord[1])
        made_move = made_move or space.is_empty()
    assert made_move
    assert game.turn == Team.BLACK

def test_end_game(game):
    assert not game._is_over()
    turns_to_end = 0
    while not game._is_over():
        game._computer_move()
        turns_to_end += 1
    assert game.winner in [Team.WHITE, Team.BLACK]

    loser = Team.WHITE if game.winner == Team.BLACK else Team.BLACK
    game.turn = loser
    assert len(game._get_possible_moves()) == 0
    print(game._display())
    assert game._is_over() 