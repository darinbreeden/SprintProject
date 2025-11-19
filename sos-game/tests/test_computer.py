# tests/test_computer.py
import unittest
from sos.models import GameMode, Letter, Player
from sos.modes import make_game
from sos.players import ComputerPlayer


class TestComputerPlayer(unittest.TestCase):

    def test_computer_takes_winning_move_if_available(self):
        g = make_game(3, GameMode.SIMPLE)
        cpu = ComputerPlayer(Player.BLUE)

        # Set up: B can win with S at (0,2)
        self.assertTrue(g.make_move(0, 0, Letter.S))  # BLUE
        self.assertTrue(g.make_move(1, 0, Letter.S))  # RED
        self.assertTrue(g.make_move(0, 1, Letter.O))  # BLUE
        self.assertTrue(g.make_move(1, 1, Letter.O))  # RED

        # Now it's BLUE's turn; computer should choose move that creates SOS
        move = cpu.choose_move(g)
        self.assertIsNotNone(move)
        r, c, letter = move
        self.assertEqual((r, c), (0, 2))
        self.assertIn(letter, (Letter.S, Letter.O))  # strategy might pick S or O, but our SOS logic expects S
        # Apply move and verify win
        g.make_move(r, c, letter)
        self.assertTrue(g.is_over)
        self.assertEqual(g.winner, Player.BLUE)

    def test_computer_can_play_full_game_without_crashing_general(self):
        g = make_game(3, GameMode.GENERAL)
        blue_cpu = ComputerPlayer(Player.BLUE)
        red_cpu = ComputerPlayer(Player.RED)

        # Set both players to CPU and simulate until board is full
        while not g.is_over:
            current = g.current_turn
            cpu = blue_cpu if current == Player.BLUE else red_cpu
            move = cpu.choose_move(g)
            self.assertIsNotNone(move)  # there should be a move until board is full
            r, c, letter = move
            self.assertTrue(g.make_move(r, c, letter))

        self.assertTrue(g.is_over)
        # Either a winner or a draw is acceptable; we just care game finishes without error


if __name__ == "__main__":
    unittest.main()
