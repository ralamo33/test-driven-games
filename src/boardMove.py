from move import Move
from piece import Piece
from pieceDirection import PieceDirection


class BoardMove():
    def __init__(self, move: Move, game):
        self.fromRow = move.fromRow
        self.fromCol = move.fromCol
        self.toRow = move.toRow
        self.toCol = move.toCol
        self.game = game
        self.from_space = self.game.get_space(self.fromRow, self.fromCol)
        self.destination_space = self.game.get_space(self.toRow, self.toCol)

        jump_row = (self.fromRow + self.toRow) // 2
        jump_col = (self.fromCol + self.toCol) // 2
        self.jump_space = self.game.get_space(jump_row, jump_col)

    def handle_move(self):
        response = self.is_valid_with_explanation() 
        if not response[0]:
            return response

        piece = self.from_space.get_piece()
        if abs(self.fromCol - self.toCol) == 2:
            return self.handle_jump(piece)
        
        self.finalize_move(piece)
        self.game.change_turn()
        return (True, "")
    
    # TODO remove self.fromRow etc.
    def is_valid_with_explanation(self):
        if self.from_space is None or self.from_space.is_empty():
            return (False, "Invalid space selected")
        if self.destination_space is None:
            return (False, "Destination not on board")
        if self.game.must_double_jump_coordinate is not None and self.game.must_double_jump_coordinate != (self.fromRow, self.fromCol):
            return (False, "Must perform double jump.")
        
        piece = self.from_space.get_piece()

        if not piece.on_team(self.game.turn):
            return (False, "It is not your turn")

        move_direction = PieceDirection.DOWN if self.toRow > self.fromRow else PieceDirection.UP
        if not piece.can_move_in_direction(move_direction):
            return (False, "Wrong direction")
        
        if not self.destination_space.is_empty():
            return (False, "Destination has another piece")
        
        if abs(self.fromCol - self.toCol) != abs(self.fromRow - self.toRow) or abs(self.fromCol - self.toCol) > 2:
            return (False, "Wrong destination")

        if abs(self.fromCol - self.toCol) == 2:
            if not self.is_valid_jump(piece,):
                return (False, "No enemy to jump over")

        return (True, "")
    
    def handle_jump(self, piece):
        if not self.is_valid_jump(piece):
            return (False, "No enemy to jump over")
        self.jump_space.delete_piece()
        self.finalize_move(piece)
        self.game.clear_double_jump()
        if self.has_double_jump():
            self.game.set_must_double_jump_next(self.toRow, self.toCol)
        else:
            self.game.change_turn() 
        return (True, "")
        
    def is_valid_jump(self, piece):
        if self.jump_space.is_empty() or not self.destination_space.is_empty():
            return False
        jump_piece = self.jump_space.get_piece()
        return piece.is_enemy(jump_piece)
    
    def has_double_jump(self):
        spots_to_check = []
        spots_to_check.append((self.toRow + 2, self.toCol + 2))
        spots_to_check.append((self.toRow + 2, self.toCol - 2))
        spots_to_check.append((self.toRow - 2, self.toCol + 2))
        spots_to_check.append((self.toRow - 2, self.toCol - 2))

        for spot in spots_to_check:
            boardMove = BoardMove(Move(self.toRow, self.toCol, spot[0], spot[1]), self.game)
            response = boardMove.is_valid_with_explanation()
            if response[0]:
                return True
        return False
        
    
    def finalize_move(self, piece: Piece):
        self.from_space.delete_piece()
        self.destination_space.add_piece(piece)
        if self.toRow == 0 or self.toRow == 7:
            piece.crown()


    