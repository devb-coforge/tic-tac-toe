from ai import AI
from board import Board


class Game:
    def __init__(self, ai: AI | None = None):
        self.board = Board()
        self._ai = ai
        self.current_mark = "X"
        self.winner = None
        self.is_draw = False

    def is_ai_turn(self) -> bool:
        return (
            self._ai is not None
            and self.current_mark == "O"
            and self.winner is None
            and not self.is_draw
        )

    def ai_move(self) -> bool:
        """Ask the selected AI for O's move and apply the usual turn rules."""
        if not self.is_ai_turn():
            return False
        row, col = self._ai.choose_move(self.board, self.current_mark)
        return self.turn(row, col)

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