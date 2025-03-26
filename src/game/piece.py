from pydantic import BaseModel
from game.piece_direction import PieceDirection
from game.team import Team


class Piece(BaseModel):
    direction: PieceDirection
    team: Team

    def is_crowned(self):
        return self.direction == PieceDirection.BOTH

    def against_team(self, team: Team):
        return self.team != team

    def on_team(self, team: Team):
        return self.team == team

    def is_enemy(self, piece):
        return self.team != piece.team

    def can_move_in_direction(self, new_direction: PieceDirection):
        return self.direction.is_valid_direction(new_direction)

    def crown(self):
        self.direction = PieceDirection.BOTH
