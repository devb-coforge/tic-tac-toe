import pytest

from game import Game


@pytest.fixture
def game():
    return Game()


def test_x_starts_the_game(game):
    assert game.current_mark == "X"
    assert game.winner is None
    assert game.is_draw is False


def test_valid_moves_alternate_marks(game):
    assert game.turn(0, 0) is True
    assert game.board.get_cell(0, 0) == "X"
    assert game.current_mark == "O"

    assert game.turn(1, 0) is True
    assert game.board.get_cell(1, 0) == "O"
    assert game.current_mark == "X"


def test_taken_cell_does_not_use_up_the_turn(game):
    game.turn(0, 0)

    result = game.turn(0, 0)

    assert result is False
    assert game.current_mark == "O"
    assert game.board.get_cell(0, 0) == "X"
    assert len(game.board.empty_cells()) == 8


@pytest.mark.parametrize("row, col", [(-1, 0), (0, -1), (3, 0), (0, 3)])
def test_off_board_move_does_not_use_up_the_turn(game, row, col):
    game.turn(0, 0)
    before = game.board.empty_cells()

    result = game.turn(row, col)

    assert result is False
    assert game.board.empty_cells() == before
    assert game.current_mark == "O"


def test_x_can_win(game):
    game.turn(0, 0)
    game.turn(1, 0)
    game.turn(0, 1)
    game.turn(1, 1)

    result = game.turn(0, 2)

    assert result is True
    assert game.winner == "X"
    assert game.is_draw is False


def test_o_can_win_and_no_more_moves_are_accepted(game):
    game.turn(0, 0)
    game.turn(1, 0)
    game.turn(0, 1)
    game.turn(1, 1)
    game.turn(2, 2)
    game.turn(1, 2)

    assert game.winner == "O"
    assert game.is_draw is False
    before = game.board.empty_cells()

    assert game.turn(2, 0) is False
    assert game.board.empty_cells() == before
    assert game.current_mark == "O"


def test_draw_ends_the_game(game):
    game.turn(0, 0)
    game.turn(0, 1)
    game.turn(0, 2)
    game.turn(1, 1)
    game.turn(1, 0)
    game.turn(1, 2)
    game.turn(2, 1)
    game.turn(2, 0)
    game.turn(2, 2)

    assert game.is_draw is True
    assert game.winner is None
    assert game.board.is_full() is True
    assert game.turn(0, 0) is False


def test_win_on_last_cell_is_not_a_draw(game):
    game.turn(0, 0)
    game.turn(0, 1)
    game.turn(0, 2)
    game.turn(1, 0)
    game.turn(1, 1)
    game.turn(1, 2)
    game.turn(2, 1)
    game.turn(2, 0)

    result = game.turn(2, 2)

    assert result is True
    assert game.board.is_full() is True
    assert game.winner == "X"
    assert game.is_draw is False
