"""
gamecore.py
------------
Defines the BaseGame abstract class, which encapsulates the core SOS logic:
- Shared attributes (board, scores, turn tracking, etc.)
- Template method for making a move
- SOS detection algorithm (horizontal, vertical, diagonal)
Subclasses (SimpleGame, GeneralGame) specialize the behavior for turn-handling and end conditions.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Tuple
from .models import Board, GameMode, Player, Letter, SOSLine


# Directions: 8 possible movement vectors around a cell (row delta, col delta)
DIRS: List[Tuple[int, int]] = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]


class BaseGame(ABC):
    """
    Base class for SOS games — provides all common functionality.

    This class follows the Template Method pattern:
      - `make_move()` is the fixed algorithm.
      - `_after_move()` is the customizable step for subclasses.
    """

    def __init__(self, size: int, mode: GameMode):
        self.mode = mode
        self.board = Board(size)
        self.current_turn: Player = Player.BLUE
        self.score = {Player.BLUE: 0, Player.RED: 0}
        self.lines: List[SOSLine] = []       # SOS patterns found
        self.winner: Player | None = None
        self.is_draw: bool = False
        self.is_over: bool = False

    # ------------------------------------------------------------------
    # Game initialization
    # ------------------------------------------------------------------
    def start_new_game(self, size: int | None = None, mode: GameMode | None = None):
        """Reset board, score, and state to start a new game."""
        if mode is not None:
            self.mode = mode
        if size is None:
            size = self.board.n
        self.board.reset(size)
        self.current_turn = Player.BLUE
        self.score = {Player.BLUE: 0, Player.RED: 0}
        self.lines.clear()
        self.winner = None
        self.is_draw = False
        self.is_over = False

    # ------------------------------------------------------------------
    # Template method: make_move
    # ------------------------------------------------------------------
    def make_move(self, r: int, c: int, letter: Letter) -> bool:
        """
        Performs one move in the SOS game.
        Returns True if the move was valid and placed successfully.
        Returns False if the move is invalid or game is over.
        """
        if self.is_over:
            return False
        if letter not in (Letter.S, Letter.O):
            return False

        placed = self.board.place(r, c, letter, self.current_turn)
        if not placed:
            return False

        # Step 1: detect all SOS created by this move
        new_lines = self._detect_sos_from(r, c)

        # Step 2: update score if new SOS found
        if new_lines:
            for ln in new_lines:
                self.lines.append(ln)
                self.score[self.current_turn] += 1

        # Step 3: delegate to subclass to handle turn and end-game logic
        self._after_move(new_lines_created=len(new_lines) > 0)
        return True

    # ------------------------------------------------------------------
    # SOS detection algorithm
    # ------------------------------------------------------------------
    def _detect_sos_from(self, r: int, c: int) -> List[SOSLine]:
        """
        Detect every new SOS line that includes the cell (r, c)
        either as start, middle, or end of the S–O–S triplet.
        Returns a list of SOSLine objects found.
        """
        out: List[SOSLine] = []
        letter = self.board.grid[r][c]

        def cell(rr: int, cc: int) -> Letter | None:
            return self.board.grid[rr][cc] if self.board.in_bounds(rr, cc) else None

        # Case 1: placed letter is 'S'
        # Check both "S at start" and "S at end" configurations.
        if letter == Letter.S:
            for dr, dc in DIRS:
                # S at start: (r,c)=S, (r+dr,c+dc)=O, (r+2dr,c+2dc)=S
                m1r, m1c = r + dr, c + dc
                e1r, e1c = r + 2*dr, c + 2*dc
                if self.board.in_bounds(e1r, e1c):
                    if cell(m1r, m1c) == Letter.O and cell(e1r, e1c) == Letter.S:
                        out.append(SOSLine(r, c, m1r, m1c, e1r, e1c, self.current_turn))

                # S at end: (r-2dr,c-2dc)=S, (r-dr,c-dc)=O, (r,c)=S
                m2r, m2c = r - dr, c - dc
                s2r, s2c = r - 2*dr, c - 2*dc
                if self.board.in_bounds(s2r, s2c):
                    if cell(m2r, m2c) == Letter.O and cell(s2r, s2c) == Letter.S:
                        out.append(SOSLine(s2r, s2c, m2r, m2c, r, c, self.current_turn))

        # Case 2: placed letter is 'O'
        # Check for S–O–S where 'O' is the middle.
        elif letter == Letter.O:
            for dr, dc in DIRS:
                s1r, s1c = r - dr, c - dc
                s2r, s2c = r + dr, c + dc
                if self.board.in_bounds(s1r, s1c) and self.board.in_bounds(s2r, s2c):
                    if cell(s1r, s1c) == Letter.S and cell(s2r, s2c) == Letter.S:
                        out.append(SOSLine(s1r, s1c, r, c, s2r, s2c, self.current_turn))

        return out

    # ------------------------------------------------------------------
    # Hook for subclasses
    # ------------------------------------------------------------------
    @abstractmethod
    def _after_move(self, new_lines_created: bool) -> None:
        """
        Subclasses implement this hook to:
        - switch turns appropriately,
        - determine when the game ends,
        - set winner/draw flags.
        """
        ...
