"""
models.py
----------
Defines the core data structures and enumerations for the SOS Game project:
- GameMode (SIMPLE or GENERAL)
- Player (BLUE or RED)
- Letter (S, O, EMPTY)
- SOSLine (dataclass for recording SOS sequences)
- Board (grid management and validation)
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List


# ----------------------------------------------------------------------
# Enumerations
# ----------------------------------------------------------------------
class GameMode(Enum):
    """Represents the two playable game modes."""
    SIMPLE = auto()
    GENERAL = auto()


class Player(Enum):
    """Represents the two players: Blue and Red."""
    BLUE = auto()
    RED = auto()

    def other(self) -> "Player":
        """Return the opposite player."""
        return Player.RED if self == Player.BLUE else Player.BLUE


class Letter(Enum):
    """Represents a cell’s state on the board."""
    EMPTY = "_"
    S = "S"
    O = "O"


# ----------------------------------------------------------------------
# Data Classes
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class SOSLine:
    """
    Represents a detected S–O–S sequence on the board.
    Stores the coordinates of the three letters and the player who made it.
    """
    r1: int
    c1: int
    r2: int
    c2: int
    r3: int
    c3: int
    owner: Player


# ----------------------------------------------------------------------
# Board Class
# ----------------------------------------------------------------------
class Board:
    """
    The Board class manages the n×n grid of Letters.
    Handles validation, placement, and reset logic.
    """

    def __init__(self, n: int):
        if n <= 2:
            raise ValueError("Board size must be greater than 2.")
        self.n = n
        # Initialize empty board
        self.grid: List[List[Letter]] = [
            [Letter.EMPTY for _ in range(n)] for _ in range(n)
        ]
        # Track which player placed each letter
        self.owner: List[List[Optional[Player]]] = [
            [None for _ in range(n)] for _ in range(n)
        ]
        self.filled_count = 0

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------
    def in_bounds(self, r: int, c: int) -> bool:
        """Check whether (r, c) is a valid coordinate on the grid."""
        return 0 <= r < self.n and 0 <= c < self.n

    def is_empty(self, r: int, c: int) -> bool:
        """Return True if the given cell is not occupied."""
        return self.grid[r][c] == Letter.EMPTY

    # ------------------------------------------------------------------
    # Gameplay methods
    # ------------------------------------------------------------------
    def place(self, r: int, c: int, letter: Letter, owner: Player) -> bool:
        """
        Attempt to place a letter in the given cell for the player.
        Returns True if successful, False if the move is invalid.
        """
        if not self.in_bounds(r, c) or not self.is_empty(r, c):
            return False
        if letter not in (Letter.S, Letter.O):
            return False

        self.grid[r][c] = letter
        self.owner[r][c] = owner
        self.filled_count += 1
        return True

    def reset(self, n: Optional[int] = None):
        """Clear the grid to start a new game. Optionally change board size."""
        if n is not None:
            if n <= 2:
                raise ValueError("Board size must be greater than 2.")
            self.n = n

        self.grid = [[Letter.EMPTY for _ in range(self.n)] for _ in range(self.n)]
        self.owner = [[None for _ in range(self.n)] for _ in range(self.n)]
        self.filled_count = 0
