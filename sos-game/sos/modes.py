"""
modes.py
---------
Defines two subclasses of BaseGame that implement the rule variations
for the Simple and General versions of the SOS game.
"""

from __future__ import annotations
from .models import GameMode, Player
from .gamecore import BaseGame


class SimpleGame(BaseGame):
    """
    Implements the 'Simple' SOS game rules:
    - The game ends immediately when any player forms the first SOS.
    - If the board fills with no SOS, it is a draw.
    - Turns alternate after every valid move.
    """

    def _after_move(self, new_lines_created: bool) -> None:
        # If a player creates an SOS, they win instantly.
        if new_lines_created and not self.is_over:
            self.winner = self.current_turn
            self.is_over = True
            return

        # Otherwise, switch turns.
        self.current_turn = self.current_turn.other()

        # Check for draw (board full, no SOS)
        if self.board.filled_count == self.board.n * self.board.n and self.winner is None:
            self.is_draw = True
            self.is_over = True


class GeneralGame(BaseGame):
    """
    Implements the 'General' SOS game rules:
    - The game continues until all cells are filled.
    - If a player forms an SOS, they take another turn immediately.
    - The winner is the player with the higher score when the board fills.
    - If scores are equal, it’s a draw.
    """

    def _after_move(self, new_lines_created: bool) -> None:
        # If no SOS was formed, alternate the turn.
        if not new_lines_created:
            self.current_turn = self.current_turn.other()
        # If SOS formed, current player gets another move — no turn change.

        # End the game when the board is completely filled.
        if self.board.filled_count == self.board.n * self.board.n:
            blue_score = self.score[Player.BLUE]
            red_score = self.score[Player.RED]

            if blue_score > red_score:
                self.winner = Player.BLUE
            elif red_score > blue_score:
                self.winner = Player.RED
            else:
                self.is_draw = True

            self.is_over = True


def make_game(size: int, mode: GameMode) -> BaseGame:
    """
    Factory function that creates either a SimpleGame or GeneralGame
    instance depending on the selected GameMode.
    """
    return SimpleGame(size, mode) if mode == GameMode.SIMPLE else GeneralGame(size, mode)
