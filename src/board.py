from move import Move, PotentialMove
from move_status import MoveStatus
from piece import Piece
from pieceDirection import PieceDirection
from space import Space
from teams import Team


class Board:
    def __init__(self):
        self.board: list[list[Space]] = []
        for _ in range(8):
            row = []
            for _ in range(8):
                row.append(Space())
            self.board.append(row)
        self._add_starting_pieces()

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

    def get_possible_moves(self, game):
        moves: list[Move] = []
        for from_row, row in enumerate(self.board):
            for from_col, space in enumerate(row):
                if space.is_empty():
                    continue
                piece = space.get_piece()
                if not piece.on_team(game.turn):
                    continue
                destinations = self._get_possible_destinations(from_row, from_col)
                for destination in destinations:
                    (to_row, to_col) = destination
                    # boardMove = BoardMove(
                    #     move=PotentialMove(fromRow, fromCol, toRow, toCol), game=game
                    # )
                    from_space = self.get_space(from_row, from_col)
                    to_space = self.get_space(to_row, to_col)
                    jump_col = (from_col + to_col) // 2
                    jump_row = (from_row + to_row) // 2
                    jump_space = self.get_space(jump_row, jump_col)
                    potential_move = PotentialMove(
                        from_row=from_row,
                        from_col=from_col,
                        from_space=from_space,
                        to_row=to_row,
                        to_col=to_col,
                        to_space=to_space,
                        jump_space=jump_space,
                    )
                    [move_status, explanation] = (
                        potential_move.is_valid_with_explanation(
                            game.turn, game.must_double_jump_coordinate
                        )
                    )
                    # [move_status, explanation] = boardMove.is_valid_with_explanation(
                    #     game.turn, game.must_double_jump_coordinate
                    # )
                    if move_status != MoveStatus.INVALID:
                        moves.append(
                            Move(
                                from_row=from_row,
                                from_col=from_col,
                                to_row=to_row,
                                to_col=to_col,
                            )
                        )
        return moves

    def _get_possible_destinations(self, row: int, col: int):
        standard_destinations = [
            (row + 1, col + 1),
            (row + 1, col + -1),
            (row + -1, col + 1),
            (row + -1, col + -1),
        ]
        jump_destinations = [
            (row + 2, col + 2),
            (row + 2, col + -2),
            (row + -2, col + 2),
            (row + -2, col + -2),
        ]
        return standard_destinations + jump_destinations

    def _add_starting_pieces(self):
        white_board = [
            self.get_space(0, 1),
            self.get_space(0, 3),
            self.get_space(0, 5),
            self.get_space(0, 7),
            self.get_space(1, 0),
            self.get_space(1, 2),
            self.get_space(1, 4),
            self.get_space(1, 6),
            self.get_space(2, 1),
            self.get_space(2, 3),
            self.get_space(2, 5),
            self.get_space(2, 7),
        ]
        black_board = [
            self.get_space(5, 0),
            self.get_space(5, 2),
            self.get_space(5, 4),
            self.get_space(5, 6),
            self.get_space(6, 1),
            self.get_space(6, 3),
            self.get_space(6, 5),
            self.get_space(6, 7),
            self.get_space(7, 0),
            self.get_space(7, 2),
            self.get_space(7, 4),
            self.get_space(7, 6),
        ]
        for space in white_board:
            space.add_piece(Piece(direction=PieceDirection.DOWN, team=Team.WHITE))

        for space in black_board:
            space.add_piece(Piece(direction=PieceDirection.UP, team=Team.BLACK))
