from game import Game
from move import Move


class Controller:

    def play_checkers(self):
        try:
            game = Game()
            while not game.is_over():
                print(game.display())
                print("\n\n")
                from_row_and_col = input("Input the row and column of the piece you want to select, seperated by a comma. You are white.\n")
                [from_row, from_col] = self.extract_row_and_col(from_row_and_col)

                to_row_and_col = input("You are white. Input the row and column of your piece's destination.\n")
                [to_row, to_col] = self.extract_row_and_col(to_row_and_col)

                try:
                    game.move(Move(from_row, from_col, to_row, to_col))
                except ValueError as e:
                    print(f"\n\n{e}\n\n")
                    continue
                else:
                    print(game.display())
                    print("\n\n")
                    game.computer_move()
                
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