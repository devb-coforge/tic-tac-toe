from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.current_mark = "X"
        self.winner = None
        self.is_draw = False

    def turn(self, row: int, col: int) -> bool:
        """Apply a move; rejected moves leave the turn unchanged."""
        if self.winner is not None or self.is_draw:
            return False
        if not self.board.place_mark(row, col, self.current_mark):
            return False

        if self.board.has_won(self.current_mark):
            self.winner = self.current_mark
        elif self.board.is_full():
            self.is_draw = True
        else:
            self.current_mark = "O" if self.current_mark == "X" else "X"

        return True