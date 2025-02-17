from typing import Optional
from pydantic import BaseModel
from piece import Piece
from teams import Team


class Space(BaseModel):
    piece: Optional[Piece] = None

    def add_piece(self, piece):
        self.piece = piece

    def delete_piece(self):
        self.piece = None

    def get_piece(self) -> Piece:
        if self.piece is None:
            raise ValueError("Piece does not exist")
        return self.piece

    def is_empty(self):
        return self.piece is None

    def display(self):
        if self.piece is None:
            return "_"
        first_letter = self.piece.team.value[0]
        if self.piece.is_crowned():
            return first_letter.upper()
        else:
            return first_letter.lower()
