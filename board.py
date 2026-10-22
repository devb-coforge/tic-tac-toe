class Board:
    def __init__(self):
        self._board_size = 3 #default 3 x 3 game only
        self._board = [["_" for _ in range(self._board_size)] for _ in range(self._board_size)]

    def get_board_size(self) -> int:
        return self._board_size

    def get_cell(self, row: int, col: int) -> str:
        return self._board[row][col]

    def _can_place(self, row: int, col: int) -> bool:
        return (
            0 <= row < self._board_size
            and 0 <= col < self._board_size
            and self._board[row][col] == "_"
        )

    def place_mark(self, row: int, col: int, mark: str) -> bool:
        """Place X or O using zero-based coordinates."""
        if not self._can_place(row, col):
            return False
        self._board[row][col] = mark
        return True

    def remove_mark(self, row: int, col: int) -> None:
        if 0 <= row < self._board_size and 0 <= col < self._board_size:
            self._board[row][col] = "_"

    def empty_cells(self) -> list[tuple[int, int]]:
        rows, cols = len(self._board), len(self._board[0])
        return [(i,j) for i in range(rows) for j in range(cols) if self._board[i][j] == "_"]
    
    def is_full(self) -> bool:
        return not self.empty_cells()

    def has_won(self, mark: str) -> bool:

        for i in range(self._board_size):
            if all(self._board[i][col] == mark for col in range(self._board_size)):
                return True
            if all(self._board[row][i] == mark for row in range(self._board_size)):
                return True

        return (
            all(self._board[i][i] == mark for i in range(self._board_size))
            or all(
                self._board[i][self._board_size - 1 - i] == mark
                for i in range(self._board_size)
            )
        )
