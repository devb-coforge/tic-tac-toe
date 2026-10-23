from random import Random

import pytest

from ai import AI, HardAI
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


class FirstEmptyAI(AI):
    def __init__(self):
        super().__init__(Random(0))
        self.calls = []

    def choose_move(self, board, mark):
        self.calls.append((board, mark))
        return board.empty_cells()[0]


def test_computer_waits_for_human_to_move():
    ai = FirstEmptyAI()
    game = Game(ai)

    assert game.is_ai_turn() is False
    assert game.ai_move() is False
    assert ai.calls == []
    assert len(game.board.empty_cells()) == 9
    assert game.current_mark == "X"


def test_computer_uses_ai_interface_to_play_o_after_human():
    ai = FirstEmptyAI()
    game = Game(ai)
    game.turn(1, 1)

    assert game.is_ai_turn() is True
    assert game.ai_move() is True

    assert ai.calls == [(game.board, "O")]
    assert game.board.get_cell(1, 1) == "X"
    assert game.board.get_cell(0, 0) == "O"
    assert game.current_mark == "X"
    assert game.is_ai_turn() is False
    assert game.ai_move() is False
    assert len(ai.calls) == 1


def test_hard_ai_plays_through_game_interface():
    game = Game(HardAI(Random(0)))
    assert game.turn(0, 0) is True

    assert game.ai_move() is True

    assert game.board.get_cell(0, 0) == "X"
    assert game.board.get_cell(1, 1) == "O"
    assert len(game.board.empty_cells()) == 7
    assert game.current_mark == "X"


def test_two_player_game_does_not_take_ai_turns(game):
    game.turn(0, 0)

    assert game.is_ai_turn() is False
    assert game.ai_move() is False
    assert game.current_mark == "O"
    assert len(game.board.empty_cells()) == 8


def test_rejected_human_move_does_not_trigger_computer():
    ai = FirstEmptyAI()
    game = Game(ai)
    game.turn(1, 1)
    game.ai_move()

    assert game.turn(1, 1) is False
    assert game.turn(-1, 0) is False
    assert game.ai_move() is False
    assert game.current_mark == "X"
    assert len(ai.calls) == 1
    assert len(game.board.empty_cells()) == 7


def test_computer_does_not_move_after_human_wins():
    ai = FirstEmptyAI()
    game = Game(ai)
    for row, col in [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)]:
        game.turn(row, col)
    before = game.board.empty_cells()

    assert game.winner == "X"
    assert game.is_ai_turn() is False
    assert game.ai_move() is False
    assert game.board.empty_cells() == before
    assert ai.calls == []


def test_computer_can_win_and_no_more_moves_are_accepted():
    ai = FirstEmptyAI()
    game = Game(ai)
    for row, col in [(1, 0), (1, 1), (2, 2)]:
        assert game.turn(row, col) is True
        assert game.ai_move() is True
    before = game.board.empty_cells()

    assert game.winner == "O"
    assert game.is_draw is False
    assert game.is_ai_turn() is False
    assert game.ai_move() is False
    assert game.turn(2, 0) is False
    assert game.board.empty_cells() == before
    assert len(ai.calls) == 3


def test_computer_does_not_move_after_draw():
    ai = FirstEmptyAI()
    game = Game(ai)
    moves = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 0), (1, 2), (2, 1), (2, 0), (2, 2)]
    for row, col in moves:
        game.turn(row, col)

    assert game.is_draw is True
    assert game.is_ai_turn() is False
    assert game.ai_move() is False
    assert game.board.is_full() is True
    assert ai.calls == []
