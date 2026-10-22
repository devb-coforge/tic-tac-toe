## Requirements

| ID | Requirement | Type | How to verify |
| --- | --- | --- | --- |
| R1 | Each new game shall start with an empty board, use X and O as marks, and give X the first turn. | Business rule | Test that a new Board has all empty cells and neither mark has won |
| R2 | The game shall alternate X and O after each accepted move while the game is in progress. | Business rule | Submit a sequence of valid moves and check that the active mark changes after each move and the marks appear in the requested cells. |
| R3 | A human player shall enter a move as two integers representing row and column (1-indexed)| Functional | Enter `2 3` and check that the mark appears in the second row, third column; verify the boundary inputs `1 1` and `3 3`. |
| R4 | An occupied or off-board cell shall be rejected without changing the board or consuming the player's turn. | Functional | Attempt an occupied cell and coordinates below 1 or above 3 through the CLI; check the message, unchanged board, and same active player. Test Board.place_mark separately with occupied cells, negative indices, and indices greater than 2; expect False and no board change. |
| R5 | Non-numeric input, blank input, or a move without exactly two integers shall show a message and let the same player try again without changing the board. | Functional | Enter `a b`, a blank line, `2`, `1 2 3`, and `1.5 2`, followed by a valid move; check that each invalid entry preserves the board and turn and that play continues. |
| R6 | The game shall announce a draw when all cells are occupied and neither player has won | Business rule | Test a full board without a winner and check that draw is announced |
| R7 | Before play begins, the player shall choose two-player or computer mode; computer mode shall assign X to the human and O to the computer and offer Easy or Hard difficulty. | Functional | Start both modes manually and check that two-player mode accepts both players' moves and that each computer difficulty moves as O after the human's X move. |
| R8 | The game shall run in a terminal on Python 3.10 or later, and will have unit-tests implemented through Pytest | Platform and verification constraint | Run the game and pytest in a clean Python 3.10-or-later environment with requirements.txt installed; check the collected test count, passing results, and every test's RNG setup. |

## Components

- **Board (`board.py`):** Initializes the empty grid in an underscore-prefixed attribute and exposes board operations through `place_mark`, `remove_mark`, `empty_cells`, `has_won`, and `is_full`.
- **AI base class (`ai.py`):** Defines the abstract `choose_move(board, mark)` contract using Python's `abc` module.
- **EasyAI (`ai.py`):** Selects a random empty cell using the `random.Random` object supplied to its constructor.
- **HardAI (`ai.py`):** Selects an optimal move with minimax while restoring the board after simulating moves.
- **Game (`game.py`):** Coordinates turns and game outcomes for two-player mode or computer mode through the Board and AI interfaces.
- **Terminal interface (`main.py`):** Handles all menus, input validation, conversion from 1-based to 0-based coordinates, and printed output.
- **Tests (`tests/`):** Verify board rules, turn handling, input behavior, and AI behavior with pytest and seeded randomness.
- **Test configuration (`conftest.py`):** Provides the root-level pytest configuration file.
- **Dependencies (`requirements.txt`):** Records the packages needed to reproduce the project's Python environment.
- **CI workflow (`.github/workflows/ci.yml`):** Runs pytest on pull requests and pushes to main.


## Decisions

### D1: Board storage

**Options considered:** A nested list of rows or a dictionary keyed by `(row, column)`.

**Chosen:** A nested list inside Board, stored in an underscore-prefixed attribute.

**Why:** Rows and columns map naturally to a 3×3 grid, and accessing the grid through Board methods keeps its representation separate from the rest of the game.

### D2: Share the AI interface

**Options considered:** One AI class with difficulty checks, or an abstract base class with EasyAI and HardAI subclasses.

**Chosen:** Use an abstract base class with `choose_move(board, mark)` and a subclass for each difficulty.

**Why:** Game can request a move through the same interface regardless of the selected difficulty. Each AI receives a `random.Random` object so tests can control randomness.


