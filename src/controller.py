from game.board import Board
from game_session import GameSession
from game.move import Move
from game.team import Team
from game.board_config import create_standard_board

class Controller:

    def play_checkers(self):
        try:
            game = GameSession(board=Board(board=create_standard_board()), team=Team.WHITE)
            while not game._is_over():
                print(game._display())
                print("\n\n")
                from_row_and_col = input(
                    "Input the row and column of the piece you want to select, seperated by a comma. You are white.\n"
                )
                [from_row, from_col] = self.extract_row_and_col(from_row_and_col)

                to_row_and_col = input(
                    "You are white. Input the row and column of your piece's destination.\n"
                )
                [to_row, to_col] = self.extract_row_and_col(to_row_and_col)

                try:
                    game.move(
                        Move(
                            from_row=from_row,
                            from_col=from_col,
                            to_row=to_row,
                            to_col=to_col,
                        )
                    )
                except ValueError as e:
                    print(f"\n\n{e}\n\n")
                    continue
                else:
                    print(game._display())
                    print("\n\n")
                    game._computer_move()

        except KeyboardInterrupt:
            print("\nThank you for playing checkers with me!")

    def extract_row_and_col(self, user_input):
        [row, col] = user_input.split(",")
        row = int(row.strip())
        col = int(col.strip())
        return [row, col]


if __name__ == "__main__":
    controller = Controller()
    controller.play_checkers()
