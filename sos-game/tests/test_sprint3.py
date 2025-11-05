"""
test_sprint3.py
----------------
Unit tests for Sprint 3 of the SOS Game project.
Covers both Simple and General game modes, including:
- Detecting SOS formation
- Handling win and draw conditions
- Managing turns and extra turns for General mode
"""

import unittest
from sos.models import GameMode, Letter, Player
from sos.modes import make_game


# ----------------------------------------------------------------------
# Simple Mode Tests
# ----------------------------------------------------------------------
class TestSimpleMode(unittest.TestCase):
    """Tests for Simple game rules."""

    def test_simple_first_sos_wins(self):
        """Verify that the first SOS immediately ends the game with the current player as winner."""
        g = make_game(3, GameMode.SIMPLE)

        # Blue forms S-O-S horizontally in the top row
        self.assertTrue(g.make_move(0, 0, Letter.S))  # Blue
        self.assertTrue(g.make_move(1, 0, Letter.S))  # Red (irrelevant)
        self.assertTrue(g.make_move(0, 1, Letter.O))  # Blue
        self.assertTrue(g.make_move(1, 1, Letter.O))  # Red
        self.assertTrue(g.make_move(0, 2, Letter.S))  # Blue creates SOS

        # Blue should win instantly
        self.assertTrue(g.is_over)
        self.assertEqual(g.winner, Player.BLUE)
        self.assertFalse(g.is_draw)

    def test_simple_draw_when_no_sos(self):
        """Verify that a draw occurs when the board fills with no SOS formed."""
        g = make_game(3, GameMode.SIMPLE)

        # Fill 3x3 board without forming SOS
        moves = [
            (0,0,Letter.O),(0,1,Letter.O),(0,2,Letter.S),
            (1,0,Letter.S),(1,1,Letter.O),(1,2,Letter.O),
            (2,0,Letter.S),(2,1,Letter.O),(2,2,Letter.S)
        ]
        for r, c, l in moves:
            self.assertTrue(g.make_move(r, c, l))

        self.assertTrue(g.is_over)
        self.assertTrue(g.is_draw)
        self.assertIsNone(g.winner)


# ----------------------------------------------------------------------
# General Mode Tests
# ----------------------------------------------------------------------
class TestGeneralMode(unittest.TestCase):
    """Tests for General game rules."""

    def test_general_extra_turn_and_winner_by_score(self):
        """Verify that the same player moves again after forming an SOS and that the final winner is correct."""
        g = make_game(3, GameMode.GENERAL)

        # Blue forms SOS horizontally in row 0
        self.assertTrue(g.make_move(0, 0, Letter.S))  # Blue
        self.assertTrue(g.make_move(1, 0, Letter.S))  # Red
        self.assertTrue(g.make_move(0, 1, Letter.O))  # Blue
        self.assertTrue(g.make_move(1, 1, Letter.O))  # Red
        self.assertTrue(g.make_move(0, 2, Letter.S))  # Blue creates SOS

        # Since Blue made SOS, Blue gets another turn
        self.assertEqual(g.current_turn, Player.BLUE)

        # Fill the rest with random letters (no additional SOS)
        for r in range(3):
            for c in range(3):
                if g.board.is_empty(r, c):
                    g.make_move(r, c, Letter.O)

        # Game should be over when full
        self.assertTrue(g.is_over)
        self.assertEqual(g.winner, Player.BLUE)
        self.assertGreaterEqual(g.score[Player.BLUE], 1)
        self.assertEqual(g.score[Player.RED], 0)

    def test_general_draw_by_equal_scores(self):
        """Verify that the game ends in a draw when both players have the same number of SOS sequences."""
        g = make_game(3, GameMode.GENERAL)

        # Fill board entirely with 'O' -> no SOS for anyone
        for r in range(3):
            for c in range(3):
                self.assertTrue(g.make_move(r, c, Letter.O))

        self.assertTrue(g.is_over)
        self.assertTrue(g.is_draw)
        self.assertEqual(g.score[Player.BLUE], 0)
        self.assertEqual(g.score[Player.RED], 0)


if __name__ == "__main__":
    unittest.main()
