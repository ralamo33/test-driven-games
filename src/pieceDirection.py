from enum import Enum

class PieceDirection(Enum):
    DOWN=0
    UP=1
    BOTH=2

    def is_valid_direction(self, direction):
        if self.name == 'BOTH':
            return True
        return self == direction