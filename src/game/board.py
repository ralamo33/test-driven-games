from typing import Any

from pydantic import BaseModel, Field

from game.space import Space
from game.board_config import create_standard_board
from game.team import Team


class Board(BaseModel):
    board: list[list[Space]] = Field(default_factory=create_standard_board)

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

    def display_htmx(self) -> str:
        """Returns HTML markup for HTMX to render the board.
        Each space is rendered as a div with appropriate classes and data attributes.
        Pieces are rendered with appropriate styling for their color and king status.
        """
        html = ['<div class="grid grid-cols-8 gap-0">']
        for i, row in enumerate(self.board):
            for j, space in enumerate(row):
                is_light = (i + j) % 2 == 0
                space_html = f'<div class="w-16 h-16 flex items-center justify-center cursor-pointer select-none transition-all duration-200 ease-in-out relative {is_light and "bg-board-light" or "bg-board-dark"}" data-row="{i}" data-col="{j}" data-selected="false">'
                
                if not space.is_empty():
                    piece = space.get_piece()
                    is_black = piece.team == Team.BLACK
                    is_king = piece.is_crowned()
                    
                    piece_html = f'<div class="w-12 h-12 rounded-full flex items-center justify-center {is_black and "bg-gray-900" or "bg-gray-100"} border-4 {is_black and "border-gray-800" or "border-white"} shadow-lg transition-transform relative {is_king and "animate-glow" or ""}">'
                    
                    if not is_king:
                        piece_html += f'<div class="absolute w-8 h-8 rounded-full {is_black and "bg-gray-800" or "bg-white"} border-2 {is_black and "border-gray-700" or "border-gray-200"}"></div>'
                    else:
                        piece_html += f'<div class="text-2xl" style="color: {is_black and "#FFD700" or "#FFA500"}">♔</div>'
                    
                    piece_html += '</div>'
                    space_html += piece_html
                
                space_html += '</div>'
                html.append(space_html)
        
        html.append('</div>')
        return '\n'.join(html)
