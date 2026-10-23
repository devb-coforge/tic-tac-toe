# Tic-Tac-Toe

A terminal Tic-Tac-Toe game for two human players or one human against an AI on a 3x3 board.

## Features

- X goes first, then players alternate after each accepted move.
- Occupied and off-board cells are rejected without using up the turn.
- The board is displayed at the start and after every accepted move.
- Wins across rows, columns, and both diagonals are detected.
- A full board without a winner ends in a draw. No further moves are accepted after a win or draw.
- Single-player mode assigns X to the human and O to the AI.
- An abstract AI class defines the move-selection interface. Subclasses inherits from it, and Game uses that interface to request computer moves.

## Setup

Use Python 3.10 or later. From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Play

```bash
python main.py
```

Choose `1` for Single Player  or `2` for Two Player. In single-player mode, you play X and the AI automatically plays O after each accepted human move, unless the game has ended.

## Tests

With the virtual environment active, run:

```bash
python -m pytest -q
```

Tests inject seeded `random.Random` instances to AI so their results are repeatable. 

