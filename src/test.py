import unittest
from boardMove import BoardMove
from game import Game
from move import Move
from piece import Piece
from pieceDirection import PieceDirection
from space import Space
from teams import Team


class TestComputerPlayer(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    # Smaller steppi
    def test_get_starting_moves(self):
        moves = self.game.get_possible_moves()
        self.assertEqual(7, len(moves))
        self.assertIn(Move(2, 1, 3, 0), moves)

    def test_advanced_moves(self):
        self.game.move(Move(2, 1, 3, 0))
        self.game.move(Move(5, 0, 4, 1))
        self.game.move(Move(2, 3, 3, 2))
        self.game.move(Move(5, 2, 4, 3))
        self.game.move(Move(1, 2, 2, 3))
        moves = self.game.get_possible_moves()
        self.assertEqual(8, len(moves))

    def test_computer_player(self):
        self.game.computer_move()
        movable_cords = [(2, 1), (2, 3), (2, 5), (2, 7)]
        made_move = False
        for cord in movable_cords:
            space = self.game.board.get_space(cord[0], cord[1])
            made_move = made_move or space.is_empty()
        self.assertTrue(made_move)
        self.assertEqual(self.game.turn, Team.BLACK)

    def test_end_game(self):
        self.assertFalse(self.game.is_over())
        turns_to_end = 0
        while not self.game.is_over():
            self.game.computer_move()
            turns_to_end += 1
        self.assertIn(self.game.winner, [Team.WHITE, Team.BLACK])

        if self.game.winner == Team.BLACK:
            loser = Team.WHITE
        else:
            loser = Team.BLACK
        self.game.turn = loser
        self.assertEqual(0, len(self.game.get_possible_moves()))
        self.assertTrue(self.game.is_over())


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_board_display(self):
        starting_display = """_ w _ w _ w _ w
w _ w _ w _ w _
_ w _ w _ w _ w
_ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _
b _ b _ b _ b _
_ b _ b _ b _ b
b _ b _ b _ b _"""
        self.assertEqual(starting_display, self.spaces.display())


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_down_valid(self):
        moving_piece = self.game.get_space(2, 1).piece
        self.game.move(Move(fromRow=2, fromCol=1, toRow=3, toCol=0))
        piece_in_new_space = self.game.get_space(3, 0).piece
        self.assertEqual(moving_piece, piece_in_new_space)
        original_space = self.game.get_space(2, 1)
        self.assertIsNone(original_space.piece)

    def test_negative_row(self):
        with self.assertRaises(ValueError) as e:
            self.game.move(Move(fromRow=2, fromCol=1, toRow=-1, toCol=0))

    def test_negative_col(self):
        with self.assertRaises(ValueError) as e:
            self.game.move(Move(fromRow=2, fromCol=1, toRow=3, toCol=-1))

    def test_wrong_direction(self):
        self.game.move(Move(fromRow=2, fromCol=1, toRow=3, toCol=0))
        with self.assertRaises(ValueError) as e:
            self.game.move(Move(fromRow=3, fromCol=0, toRow=2, toCol=1))

        self.game.move(Move(5, 0, 4, 1))
        with self.assertRaises(ValueError) as e:
            self.game.move(Move(4, 1, 5, 0))

    def test_destination_over_board(self):
        with self.assertRaises(ValueError) as e:
            self.game.move(Move(fromRow=2, fromCol=7, toRow=3, toCol=8))

    def test_invalid_move_on_board(self):
        fromRow = 2
        fromCol = 1
        side_length = 8
        for toRow in range(side_length):
            for toCol in range(side_length):
                if toRow == 3 and toCol in [0, 2]:
                    continue
                with self.assertRaises(ValueError) as e:
                    self.game.move(Move(fromRow, fromCol, toRow, toCol))

    def test_destination_has_another_piece(self):
        with self.assertRaises(ValueError) as e:
            self.game.move(Move(0, 1, 1, 0))
        self.assertEqual(str(e.exception), "Destination has another piece")

    def test_eat_enemy(self):
        self.game.move(Move(2, 1, 3, 0))
        self.game.move(Move(5, 0, 4, 1))
        self.game.move(Move(2, 3, 3, 2))
        self.game.move(Move(5, 2, 4, 3))
        self.game.move(Move(1, 2, 2, 3))

        orginal_piece = self.game.get_space(4, 3).piece
        self.game.move(Move(4, 3, 2, 1))
        self.assertEqual(orginal_piece, self.game.get_space(2, 1).piece)
        self.assertIsNone(self.game.get_space(3, 2).piece)
        self.assertIsNone(self.game.get_space(4, 3).piece)
        self.game.move(Move(2, 3, 3, 4))

    def test_cannot_eat_if_destination_filled(self):
        self.game.move(Move(2, 1, 3, 0))
        self.game.move(Move(5, 0, 4, 1))
        self.game.move(Move(2, 3, 3, 2))
        self.game.move(Move(5, 2, 4, 3))
        self.game.move(Move(1, 0, 2, 1))
        self.game.move(Move(5, 6, 4, 7))

        with self.assertRaises(ValueError) as e:
            self.game.move(Move(3, 2, 5, 4))
        self.assertEqual(str(e.exception), "Destination has another piece")

    def test_cannot_eat_friend(self):
        self.game.move(Move(2, 1, 3, 0))
        self.game.move(Move(5, 0, 4, 1))
        self.game.move(Move(2, 3, 3, 2))
        self.game.move(Move(5, 2, 4, 3))
        self.game.move(Move(1, 0, 2, 1))
        with self.assertRaises(ValueError) as e:
            self.game.move(Move(6, 7, 4, 5))
        self.assertEqual(str(e.exception), "No enemy to jump over")

    def test_player_cannot_go_twice(self):
        self.game.move(Move(2, 1, 3, 0))
        with self.assertRaises(ValueError) as e:
            self.game.move(Move(3, 0, 4, 1))
        self.assertEqual(str(e.exception), "It is not your turn")


class CrownedTest(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.move(Move(2, 1, 3, 0))
        self.game.move(Move(5, 0, 4, 1))
        self.game.move(Move(2, 3, 3, 2))
        self.game.move(Move(5, 2, 4, 3))
        self.game.move(Move(1, 2, 2, 3))
        self.game.move(Move(4, 3, 2, 1))
        self.game.move(Move(1, 0, 3, 2))
        self.game.move(Move(3, 2, 5, 0))
        self.game.move(Move(5, 4, 4, 3))

        self.game.move(Move(0, 1, 1, 2))
        self.game.move(Move(4, 3, 3, 2))
        self.game.move(Move(2, 3, 3, 4))

        self.game.move(Move(3, 2, 2, 1))
        self.game.move(Move(2, 5, 3, 6))
        self.game.move(Move(2, 1, 1, 0))
        self.game.move(Move(3, 6, 4, 7))
        self.game.move(Move(1, 0, 0, 1))

        self.crowned_space = self.game.get_space(0, 1)
        self.crowned_piece = self.crowned_space.piece

    def test_crown_piece(self):
        self.assertEqual(self.crowned_piece.direction, PieceDirection.BOTH)
        self.assertEqual(self.crowned_space.display(), "B")

    def test_triple_jump_with_crown(self):
        self.game.move(Move(2, 7, 3, 6))
        self.game.move(Move(0, 1, 2, 3))
        self.game.move(Move(2, 3, 4, 5))
        self.assertEqual(self.game.turn, Team.BLACK)
        self.game.move(Move(4, 5, 2, 7))


class DoubleJumpTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.move(Move(2, 1, 3, 0))
        self.game.move(Move(5, 0, 4, 1))
        self.game.move(Move(2, 3, 3, 2))
        self.game.move(Move(5, 2, 4, 3))
        self.game.move(Move(1, 2, 2, 3))
        self.game.move(Move(4, 3, 2, 1))

    def test_double_jump(self):
        double_jump_piece = self.game.get_space(1, 0).piece
        self.game.move(Move(1, 0, 3, 2))
        self.game.move(Move(3, 2, 5, 0))
        self.assertEqual(double_jump_piece, self.game.get_space(5, 0).get_piece())
        self.assertTrue(self.game.get_space(2, 1).is_empty())
        self.assertTrue(self.game.get_space(4, 1).is_empty())
        self.game.move(Move(5, 4, 4, 3))

    def test_invalid_double_jump_move(self):
        self.game.move(Move(1, 0, 3, 2))
        with self.assertRaises(ValueError) as e:
            self.game.move(Move(3, 0, 5, 2))
        self.assertEqual(str(e.exception), "Must perform double jump.")


class TestSpace(unittest.TestCase):
    def setUp(self):
        self.white_piece = Piece(direction=PieceDirection.DOWN, team=Team.WHITE)
        self.black_piece = Piece(direction=PieceDirection.UP, team=Team.BLACK)

    def test_blank_space(self):
        space = Space()
        space_display = space.display()
        self.assertEqual("_", space_display)

    def test_white_space(self):
        space = Space()
        space.add_piece(self.white_piece)
        self.assertEqual("w", space.display())

    def test_black_space(self):
        space = Space()
        space.add_piece(self.black_piece)
        self.assertEqual("b", space.display())

    def test_is_empty(self):
        space = Space()
        self.assertTrue(space.is_empty())
        space.add_piece(self.white_piece)
        self.assertFalse(space.is_empty())


class TestPieceDirection(unittest.TestCase):
    def test_direction_is_valid(self):
        self.assertTrue(PieceDirection.UP.is_valid_direction(PieceDirection.UP))
        self.assertTrue(PieceDirection.DOWN.is_valid_direction(PieceDirection.DOWN))
        self.assertTrue(PieceDirection.BOTH.is_valid_direction(PieceDirection.UP))
        self.assertTrue(PieceDirection.BOTH.is_valid_direction(PieceDirection.DOWN))


class TestPiece(unittest.TestCase):

    def setUp(self):
        self.piece = Piece(direction=PieceDirection.DOWN, team=Team.WHITE)
        self.upPiece = Piece(direction=PieceDirection.UP, team=Team.BLACK)

    def test_direction(self):
        self.assertTrue(self.piece.can_move_in_direction(PieceDirection.DOWN))
        self.assertFalse(self.piece.can_move_in_direction(PieceDirection.UP))

    def test_team(self):
        self.assertTrue(self.piece.on_team(Team.WHITE))
        self.assertFalse(self.piece.on_team(Team.BLACK))

    def test_against_team(self):
        self.assertTrue(self.piece.against_team(Team.BLACK))
        self.assertFalse(self.piece.against_team(Team.WHITE))

    def test_is_enemy(self):
        self.assertTrue(self.piece.is_enemy(self.upPiece))
        self.assertFalse(self.piece.is_enemy(self.piece))


if __name__ == "__main__":
    unittest.main()
