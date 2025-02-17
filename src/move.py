from dataclasses import dataclass

@dataclass
class Move:
    fromRow: int
    fromCol: int
    toRow: int
    toCol: int