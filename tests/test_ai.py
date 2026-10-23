from random import Random

import pytest

from ai import AI, EasyAI
from board import Board


def board_state(board):
    size = board.get_board_size()
    return [[board.get_cell(row, col) for col in range(size)] for row in range(size)]


def test_abstract_ai_cannot_be_created():
    with pytest.raises(TypeError):
        AI(Random(0))


@pytest.mark.parametrize("seed", [0, 1, 7, 42])
@pytest.mark.parametrize("mark", ["X", "O"])
def test_easy_chooses_empty_cells_without_changing_board(seed, mark):
    board = Board()
    ai = EasyAI(Random(seed))

    for _ in range(9):
        empty_cells = board.empty_cells()
        before = board_state(board)

        move = ai.choose_move(board, mark)

        assert move in empty_cells
        assert board_state(board) == before
        assert board.place_mark(*move, mark) is True


@pytest.mark.parametrize("seed", [0, 1, 7, 42])
def test_easy_uses_supplied_generator_and_repeats_with_same_seed(seed):
    board = Board()
    board.place_mark(0, 0, "X")
    board.place_mark(1, 1, "O")
    expected_rng = Random(seed)
    first_ai = EasyAI(Random(seed))
    second_ai = EasyAI(Random(seed))

    for _ in range(5):
        expected = expected_rng.choice(board.empty_cells())

        assert first_ai.choose_move(board, "O") == expected
        assert second_ai.choose_move(board, "O") == expected


def test_easy_chooses_only_remaining_cell():
    board = Board()
    for row, col in board.empty_cells():
        if (row, col) != (2, 1):
            board.place_mark(row, col, "X")

    assert EasyAI(Random(0)).choose_move(board, "O") == (2, 1)


def test_easy_rejects_a_full_board_without_changing_it():
    board = Board()
    for row, col in board.empty_cells():
        board.place_mark(row, col, "X")
    before = board_state(board)

    with pytest.raises(ValueError, match="full board"):
        EasyAI(Random(0)).choose_move(board, "O")

    assert board_state(board) == before
