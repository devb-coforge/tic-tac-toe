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
