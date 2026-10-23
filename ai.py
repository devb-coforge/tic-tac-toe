from abc import ABC, abstractmethod
from random import Random

from board import Board


class AI(ABC):
    """Shared interface for computer players."""

    def __init__(self, rng: Random | None = None):
        self._rng = rng if rng is not None else Random()

    @abstractmethod
    def choose_move(self, board: Board, mark: str) -> tuple[int, int]:
        """Should be implemented by the subclass"""
        pass


class EasyAI(AI):
    def choose_move(self, board: Board, mark: str) -> tuple[int, int]:
        empty_cells = board.empty_cells()
        if not empty_cells:
            raise ValueError("Cannot choose a move on a full board.")
        return self._rng.choice(empty_cells)


class HardAI(AI):
    def choose_move(self, board: Board, mark: str) -> tuple[int, int]:
        empty_cells = board.empty_cells()
        
        opponent = "O" if mark == "X" else "X"
        store = {} #store the game tree for fast look up
        move_scores = []
        for row, col in empty_cells:
            board.place_mark(row, col, mark)
            score = self._minimax(board, opponent, mark, 1, store)
            board.remove_mark(row, col)
            move_scores.append((score, (row, col)))

        best_score = max(score for score, _ in move_scores)
        best_moves = [move for score, move in move_scores if score == best_score]
        return self._rng.choice(best_moves)

    def _minimax(
        self,
        board: Board,
        current_mark: str,
        ai_mark: str,
        depth: int,
        store: dict[tuple, int],
    ) -> int:
        """Score each position assuming both players choose their best move."""
        opponent = "O" if ai_mark == "X" else "X"
        if board.has_won(ai_mark): #AI has won, return a high score
            return 10 - depth
        if board.has_won(opponent): #Opponent has won, return a low score
            return depth - 10

        empty_cells = board.empty_cells()
        if not empty_cells: #Return a draw
            return 0

        size = board.get_board_size()
        state = (
            current_mark,
            depth,
            tuple(board.get_cell(row, col) for row in range(size) for col in range(size)),
        )
        if state in store:
            return store[state]

        next_mark = "O" if current_mark == "X" else "X"
        scores = []
        for row, col in empty_cells:
            board.place_mark(row, col, current_mark)

            #recursive call to the minimax function
            scores.append(self._minimax(board, next_mark, ai_mark, depth + 1, store))

            board.remove_mark(row, col) #backtrack

        score = max(scores) if current_mark == ai_mark else min(scores) #If AI is the current mark, we want to maximize the score, otherwise minimize the score.
        store[state] = score
        return score
