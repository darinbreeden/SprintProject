from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple, Optional
import random

from .models import Player, Letter
from .gamecore import BaseGame


class AbstractPlayer(ABC):
    """Base class for different kinds of players (human or computer)."""

    def __init__(self, identity: Player):
        self.identity = identity

    @abstractmethod
    def is_human(self) -> bool:
        ...


class HumanPlayer(AbstractPlayer):
    """Represents a human player; moves are driven by GUI events."""

    def is_human(self) -> bool:
        return True


class ComputerPlayer(AbstractPlayer):
    """
    Simple computer opponent.

    Strategy:
      1. If there is a move that creates at least one SOS, take it.
      2. Otherwise, pick the first available cell and place 'S'.
    This is not optimal, but it can win if a winning move exists.
    """

    def is_human(self) -> bool:
        return False

    def choose_move(self, game: BaseGame) -> Optional[Tuple[int, int, Letter]]:
        # Ensure we are thinking as *this* player
        original_turn = game.current_turn
        game.current_turn = self.identity

        try:
            # 1. Try to find a winning move that creates SOS
            move = self._find_winning_move(game)
            if move is not None:
                return move

            # 2. Fallback: first empty cell with 'S'
            for r in range(game.board.n):
                for c in range(game.board.n):
                    if game.board.is_empty(r, c):
                        return (r, c, Letter.S)

            # No moves available (board full)
            return None
        finally:
            game.current_turn = original_turn

    def _find_winning_move(self, game: BaseGame) -> Optional[Tuple[int, int, Letter]]:
        """
        Search all empty cells and letters S/O.
        If placing a letter there would create any SOS for this player, return that move.
        """
        for r in range(game.board.n):
            for c in range(game.board.n):
                if not game.board.is_empty(r, c):
                    continue

                for letter in (Letter.S, Letter.O):
                    if self._would_create_sos(game, r, c, letter):
                        return (r, c, letter)
        return None

    def _would_create_sos(self, game: BaseGame, r: int, c: int, letter: Letter) -> bool:
        """
        Temporarily place a letter, run SOS detection, then revert.
        Returns True if at least one SOS would be formed.
        """
        board = game.board

        # Save original state
        orig_letter = board.grid[r][c]
        orig_owner = board.owner[r][c]
        orig_filled = board.filled_count

        # Simulate placement
        board.grid[r][c] = letter
        board.owner[r][c] = self.identity
        board.filled_count += 1

        try:
            new_lines = game._detect_sos_from(r, c)  # using BaseGame's logic
            return len(new_lines) > 0
        finally:
            # Revert board
            board.grid[r][c] = orig_letter
            board.owner[r][c] = orig_owner
            board.filled_count = orig_filled