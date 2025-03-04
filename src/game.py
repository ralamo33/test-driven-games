import random
from typing import Optional

from pydantic import BaseModel

from board import Board
from boardMove import BoardMove
from move import Move
from space import Space
from move_status import MoveStatus
from teams import Team


class Game(BaseModel):
    board: Board = Board()
    turn: Team = Team.WHITE
    must_double_jump_coordinate: Optional[tuple[int, int]] = None
    winner: Optional[Team] = None
    
    def move(self, move: Move):
        current_team = self.turn
        board_move = BoardMove(from_row=move.from_row, from_col=move.from_col, to_row=move.to_row, to_col=move.to_col,
                               board=self.board, active_team=self.turn, must_double_jump_coordinate=self.must_double_jump_coordinate)
        (move_status, message) = board_move.handle_move()
        self.clear_double_jump()
        match move_status:
            case MoveStatus.INVALID:
                raise ValueError(message)
            case MoveStatus.MOVE | MoveStatus.JUMP:
                self.change_turn()
            case MoveStatus.JUMP_WITH_DOUBLE_JUMP:
                self.must_double_jump_coordinate = (board_move.to_row, board_move.to_col)
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
