import random
from board import Board
from boardMove import BoardMove
from move import Move
from space import Space
from teams import Team

class Game():
    
    def __init__(self):
        self.board = Board()
        self.turn = Team.WHITE
        self.must_double_jump_coordinate = None
        self.winner = None
    
    def move(self, move: Move):
        current_team = self.turn
        boardMove = BoardMove(move, self)
        (is_valid, message) = boardMove.handle_move()
        if not is_valid:
            raise ValueError(message)
        if len(self.get_possible_moves()) == 0:
            self.winner = current_team

    def get_space(self, row, col) -> Space:
        return self.board.get_space(row, col)

    def display(self):
        return self.board.display()

    def set_must_double_jump_next(self, row, col):
        self.must_double_jump_coordinate = (row, col)
    
    def clear_double_jump(self):
        self.must_double_jump_coordinate = None
    
    def change_turn(self):
        self.must_double_jump_coordinate = None
        if self.turn == Team.WHITE:
            self.turn = Team.BLACK
        else:
            self.turn = Team.WHITE
    
    def get_possible_moves(self):
        return self.board.get_possible_moves(self) 

    def is_over(self):
        return self.winner is not None

    def computer_move(self):
        if self.winner is not None:
            return
        possible_moves = self.get_possible_moves()
        self.move(random.choice(possible_moves))

