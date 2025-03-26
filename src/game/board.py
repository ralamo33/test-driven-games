from typing import Any

from pydantic import BaseModel, Field

from game.space import Space
from game.board_config import create_standard_board


class Board(BaseModel):
    board: list[list[Space]] = Field(default_factory=list)

    def __init__(self, **data):
        super().__init__(**data)
        if not self.board:
            self.board = create_standard_board()

    def get_space(self, row, col) -> Space:
        row_len = len(self.board)
        col_len = len(self.board[0])
        if row >= 0 and col >= 0 and row < row_len and col < col_len:
            return self.board[row][col]
        return None

    def display(self):
        display_str = ""
        for row in self.board:
            for space in row:
                display_str += space.display()
                display_str += " "
            display_str = display_str[:-1]
            display_str += "\n"
        display_str = display_str[:-1]
        return display_str
