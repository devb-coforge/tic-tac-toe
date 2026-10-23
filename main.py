from random import Random

from ai import EasyAI, HardAI
from game import Game


def get_mode():
    print("Please select a mode:")
    print("1. Single Player")
    print("2. Two Player")
    while True:
        mode = input("Enter your choice: ").strip()
        if mode == "2":
            print("You have selected Two Player")
            return "two"
        if mode == "1":
            print("You have selected Single Player")
            print("You play X. The computer plays O.")
            return "single"
        else:
            print("Invalid choice")


def get_difficulty():
    print("Please select a difficulty:")
    print("1. Easy")
    print("2. Hard")
    while True:
        difficulty = input("Enter your choice: ").strip()
        if difficulty == "1":
            print("You have selected Easy AI")
            return "easy"
        if difficulty == "2":
            print("You have selected Hard AI")
            return "hard"
        print("Invalid choice")


def get_user_input(mark: str) -> tuple[int, int]:
    while True:
        move = input(f"{mark}, enter row and column (1-3), e.g. 2 3: ")
        parts = move.split()
        if len(parts) != 2:
            print("Enter exactly two whole numbers, e.g. 2 3")
            continue
        row, col = parts
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
    mode = get_mode()
    ai = None
    if mode == "single":
        difficulty = get_difficulty()
        ai = EasyAI(Random()) if difficulty == "easy" else HardAI(Random())
    game = Game(ai)
    print_board(game.board)

    while game.winner is None and not game.is_draw:
        if game.is_ai_turn():
            print("AI (O) is choosing a move...")
            game.ai_move()
        else:
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
