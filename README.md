# Tic-Tac-Toe

A terminal Tic-Tac-Toe game for two human players on a 3x3 board.

## Implemented

- X goes first, then players alternate after each accepted move.
- Occupied and off-board cells are rejected without using up the turn.
- The board is displayed at the start and after every accepted move.
- Wins across rows, columns, and both diagonals are detected.
- A full board without a winner ends in a draw. No further moves are accepted after a win or draw.

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

Choose `2` for Two Player. On each turn, enter a row and column from 1 to 3, separated by a space. For example, `2 3` places a mark in the second row, third column. Empty cells appear as `_`.

## Tests

With the virtual environment active, run:

```bash
python -m pytest -q
```

