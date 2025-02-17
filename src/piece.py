from pieceDirection import PieceDirection
from teams import Team

class Piece:
    def __init__(self, direction: PieceDirection, team: Team):
        self.direction = direction
        self.team = team
    
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
 