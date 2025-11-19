"""
test_game.py
-------------
Unit tests for the SOS game's core logic (Sprint 2).
Verifies correct initialization, move handling, and turn switching
for both players in Simple mode.
"""

import unittest
from sos.modes import make_game
from sos.models import GameMode, Letter, Player


class TestGameSprint2(unittest.TestCase):
    """Tests for initial game setup and basic S/O placement."""

    def test_new_game_initial_state(self):
        """Ensure a new game starts with an empty board and Blue's turn."""
        g = make_game(5, GameMode.GENERAL)
        self.assertEqual(g.board.n, 5)
        self.assertEqual(g.mode, GameMode.GENERAL)
        self.assertEqual(g.current_turn, Player.BLUE)
        self.assertEqual(g.board.filled_count, 0)
        self.assertFalse(g.is_over)
        self.assertEqual(g.score[Player.BLUE], 0)
        self.assertEqual(g.score[Player.RED], 0)

    def test_make_move_places_letter_and_switches_turn_simple(self):
        """Ensure moves correctly place letters and alternate turns in Simple mode."""
        g = make_game(3, GameMode.SIMPLE)

        # Blue places S
        self.assertTrue(g.make_move(0, 0, Letter.S))
        self.assertEqual(g.board.grid[0][0], Letter.S)
        self.assertEqual(g.current_turn, Player.RED)

        # Red places O
        self.assertTrue(g.make_move(0, 1, Letter.O))
        self.assertEqual(g.board.grid[0][1], Letter.O)
        self.assertEqual(g.current_turn, Player.BLUE)

    def test_cannot_overwrite_cell(self):
        """Ensure a player cannot overwrite an occupied cell."""
        g = make_game(3, GameMode.SIMPLE)

        # Blue places S
        self.assertTrue(g.make_move(0, 0, Letter.S))
        # Red tries to overwrite same cell
        self.assertFalse(g.make_move(0, 0, Letter.O))
        # The board should remain unchanged
        self.assertEqual(g.board.grid[0][0], Letter.S)

        # Red still gets to move in a valid cell
        self.assertTrue(g.make_move(0, 1, Letter.O))
        self.assertEqual(g.board.grid[0][1], Letter.O)
        self.assertEqual(g.current_turn, Player.BLUE)


if __name__ == "__main__":
    unittest.main()
