"""
ui.py
------
Tkinter graphical interface for the SOS game.
Supports:
- Simple and General game modes
- Variable board sizes
- Player letter choices (S or O)
- New Game button
- Turn tracking, score display, and winner/draw alerts
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .models import GameMode, Player, Letter
from .modes import make_game


class SOSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SOS - Sprint 3")
        self.geometry("720x620")

        # Default game (SIMPLE mode, 3×3 board)
        self.mode_var = tk.StringVar(value="SIMPLE")
        self.size_var = tk.IntVar(value=3)
        self.game = make_game(self.size_var.get(), GameMode.SIMPLE)

        # Create GUI layout
        self._build_controls()
        self._build_player_panels()
        self.board_frame = ttk.Frame(self)
        self.board_frame.pack(pady=10)
        self.board_buttons = []
        self._build_board()

        # Status/score display
        self.status_var = tk.StringVar(value=self._status_text())
        ttk.Label(self, textvariable=self.status_var, font=("Arial", 12)).pack(pady=8)

    # ------------------------------------------------------------------
    # GUI Component Builders
    # ------------------------------------------------------------------
    def _build_controls(self):
        frame = ttk.Frame(self)
        frame.pack(pady=10, fill="x")

        ttk.Label(frame, text="Game Mode:").grid(row=0, column=0, padx=6, sticky="w")
        ttk.Radiobutton(frame, text="Simple", variable=self.mode_var, value="SIMPLE").grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(frame, text="General", variable=self.mode_var, value="GENERAL").grid(row=0, column=2, sticky="w")

        ttk.Label(frame, text="Board Size:").grid(row=0, column=3, padx=(20, 6), sticky="w")
        size_spin = ttk.Spinbox(frame, from_=3, to=12, textvariable=self.size_var, width=5)
        size_spin.grid(row=0, column=4, sticky="w")

        ttk.Button(frame, text="New Game", command=self.on_new_game).grid(row=0, column=5, padx=12)

    def _build_player_panels(self):
        container = ttk.Frame(self)
        container.pack(pady=6, fill="x")

        # Blue player controls
        blue = ttk.LabelFrame(container, text="Blue Player")
        blue.pack(side="left", padx=10)
        self.blue_letter = tk.StringVar(value="S")
        ttk.Radiobutton(blue, text="S", value="S", variable=self.blue_letter).pack(anchor="w")
        ttk.Radiobutton(blue, text="O", value="O", variable=self.blue_letter).pack(anchor="w")

        # Red player controls
        red = ttk.LabelFrame(container, text="Red Player")
        red.pack(side="left", padx=10)
        self.red_letter = tk.StringVar(value="S")
        ttk.Radiobutton(red, text="S", value="S", variable=self.red_letter).pack(anchor="w")
        ttk.Radiobutton(red, text="O", value="O", variable=self.red_letter).pack(anchor="w")

        # Legend / instructions
        legend = ttk.LabelFrame(container, text="Legend")
        legend.pack(side="left", padx=10)
        ttk.Label(legend, text="Click a cell to place your selected letter.").pack(anchor="w", padx=8, pady=4)

    def _build_board(self):
        # Clear any previous board
        for row in self.board_buttons:
            for btn in row:
                btn.destroy()
        self.board_buttons = []

        n = self.game.board.n
        for r in range(n):
            row_btns = []
            for c in range(n):
                btn = ttk.Button(
                    self.board_frame,
                    text=" ",
                    width=4,
                    command=lambda rr=r, cc=c: self.on_cell_click(rr, cc)
                )
                btn.grid(row=r, column=c, padx=2, pady=2)
                row_btns.append(btn)
            self.board_buttons.append(row_btns)

        self._refresh_board_text()

    # ------------------------------------------------------------------
    # Event Handlers
    # ------------------------------------------------------------------
    def on_new_game(self):
        """Start a new game with selected mode and size."""
        size = max(3, int(self.size_var.get()))
        mode = GameMode.SIMPLE if self.mode_var.get() == "SIMPLE" else GameMode.GENERAL
        self.game = make_game(size, mode)
        self.game.start_new_game(size=size, mode=mode)
        self._build_board()
        self._update_status()

    def on_cell_click(self, r: int, c: int):
        """Handle cell clicks from players."""
        if self.game.is_over:
            messagebox.showinfo("Game Over", "Start a new game to play again.")
            return

        curr = self.game.current_turn
        letter_choice = self.blue_letter.get() if curr == Player.BLUE else self.red_letter.get()
        letter = Letter.S if letter_choice == "S" else Letter.O

        if not self.game.make_move(r, c, letter):
            messagebox.showwarning("Invalid Move", "That cell is already occupied.")
            return

        self._refresh_board_text()
        self._update_status()

        # End-of-game check
        if self.game.is_over:
            if self.game.is_draw:
                messagebox.showinfo("Result", "Game ended in a draw.")
            else:
                winner = "Blue" if self.game.winner == Player.BLUE else "Red"
                messagebox.showinfo("Result", f"{winner} wins!")

    # ------------------------------------------------------------------
    # Utility / Display Methods
    # ------------------------------------------------------------------
    def _refresh_board_text(self):
        """Update the button text to reflect the board’s current state."""
        n = self.game.board.n
        for r in range(n):
            for c in range(n):
                val = self.game.board.grid[r][c].value
                self.board_buttons[r][c].configure(text=val if val != "_" else " ")

    def _status_text(self) -> str:
        """Return current status string (turn, score, winner)."""
        b = self.game.score[Player.BLUE]
        r = self.game.score[Player.RED]

        if self.game.is_over:
            if self.game.is_draw:
                return f"Scores — Blue: {b}  Red: {r}   Result: Draw"
            else:
                winner = "Blue" if self.game.winner == Player.BLUE else "Red"
                return f"Scores — Blue: {b}  Red: {r}   Winner: {winner}"

        turn = "Blue" if self.game.current_turn == Player.BLUE else "Red"
        return f"Scores — Blue: {b}  Red: {r}   Current turn: {turn}"

    def _update_status(self):
        """Refresh the status label text."""
        self.status_var.set(self._status_text())


# ----------------------------------------------------------------------
# Run as a standalone program
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = SOSApp()
    app.mainloop()
