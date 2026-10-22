import pytest

from board import Board


@pytest.fixture
def board():
    return Board()


def test_new_board_is_empty(board):
    assert board.get_board_size() == 3
    assert len(board.empty_cells()) == 9
    assert board.is_full() is False


@pytest.mark.parametrize("mark", ["X", "O"])
def test_new_board_has_no_winner(board, mark):
    assert board.has_won(mark) is False


def test_place_mark_puts_mark_on_cell(board):
    result = board.place_mark(1, 2, "X")

    assert result is True
    assert board.get_cell(1, 2) == "X"
    assert (1, 2) not in board.empty_cells()
    assert len(board.empty_cells()) == 8


def test_taken_cell_is_rejected_and_first_mark_stays(board):
    board.place_mark(0, 0, "X")

    result = board.place_mark(0, 0, "O")

    assert result is False
    assert board.get_cell(0, 0) == "X"
    assert len(board.empty_cells()) == 8


@pytest.mark.parametrize("row, col", [(-1, 0), (0, -1), (3, 0), (0, 3)])
def test_off_board_move_is_rejected(board, row, col):
    result = board.place_mark(row, col, "X")

    assert result is False
    assert len(board.empty_cells()) == 9


def test_remove_mark_makes_cell_available_again(board):
    board.place_mark(1, 2, "X")

    board.remove_mark(1, 2)

    assert board.get_cell(1, 2) == "_"
    assert (1, 2) in board.empty_cells()
    assert len(board.empty_cells()) == 9


@pytest.mark.parametrize("row", [0, 1, 2])
def test_three_marks_across_a_row_win(board, row):
    board.place_mark(row, 0, "X")
    board.place_mark(row, 1, "X")
    board.place_mark(row, 2, "X")

    assert board.has_won("X") is True
    assert board.has_won("O") is False


@pytest.mark.parametrize("col", [0, 1, 2])
def test_three_marks_down_a_column_win(board, col):
    board.place_mark(0, col, "O")
    board.place_mark(1, col, "O")
    board.place_mark(2, col, "O")

    assert board.has_won("O") is True
    assert board.has_won("X") is False


def test_top_left_to_bottom_right_diagonal_wins(board):
    board.place_mark(0, 0, "X")
    board.place_mark(1, 1, "X")
    board.place_mark(2, 2, "X")

    assert board.has_won("X") is True


def test_top_right_to_bottom_left_diagonal_wins(board):
    board.place_mark(0, 2, "O")
    board.place_mark(1, 1, "O")
    board.place_mark(2, 0, "O")

    assert board.has_won("O") is True


def test_two_marks_in_a_row_do_not_win(board):
    board.place_mark(0, 0, "X")
    board.place_mark(0, 1, "X")

    assert board.has_won("X") is False


def test_full_board_without_winner(board):
    board.place_mark(0, 0, "X")
    board.place_mark(0, 1, "O")
    board.place_mark(0, 2, "X")
    board.place_mark(1, 0, "X")
    board.place_mark(1, 1, "O")
    board.place_mark(1, 2, "O")
    board.place_mark(2, 0, "O")
    board.place_mark(2, 1, "X")
    board.place_mark(2, 2, "X")

    assert board.is_full() is True
    assert board.empty_cells() == []
    assert board.has_won("X") is False
    assert board.has_won("O") is False
