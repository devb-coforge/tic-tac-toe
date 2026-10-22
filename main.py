from game import Game


def get_mode():
    print("Please select a mode:")
    print("1. Single Player (not available yet)")
    print("2. Two Player")
    while True:
        mode = input("Enter your choice: ").strip()
        if mode == "2":
            print("You have selected Two Player")
            return "two"
        if mode == "1":
            print("Single Player is not available yet.")
            pass
        else:
            print("Invalid choice")


def get_user_input(mark: str) -> tuple[int, int]:
    while True:
        move = input(f"{mark}, enter row and column (1-3), e.g. 2 3: ")
        row, col = move.split()
        if not row.isdigit() or not col.isdigit():
            print("Enter exactly two whole numbers, e.g. 2 3")
            continue
        row_int, col_int = int(row), int(col)
        if not (1 <= row_int <= 3 and 1 <= col_int <= 3):
            print("Row and column must be in between 1 and 3")
            continue

        return row_int - 1, col_int - 1 #return 0 indexed


def print_board(board):
    size = board.get_board_size()
    print("  " + " ".join(str(col + 1) for col in range(size)))
    for row in range(size):
        print(f"{row + 1} " + " ".join(board.get_cell(row, col) for col in range(size)))
    print() #new line


def main():
    print("Welcome to Tic Tac Toe!")
    _ = get_mode() #will add single vs two player mode here
    game = Game()
    print_board(game.board)

    while game.winner is None and not game.is_draw:
        row, col = get_user_input(game.current_mark)
        if not game.turn(row, col):
            print("That cell is taken. Try again.")
            continue
        print_board(game.board)

    if game.winner is not None:
        print(f"{game.winner} has won!")
    else:
        print("Draw!")


if __name__ == "__main__":
    main()
