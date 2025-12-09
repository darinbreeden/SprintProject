# sos/recorder.py
"""
recorder.py
------------
Provides support for recording and replaying SOS games from/to a text file.

File format (simple text):

    # SOS recording v1
    MODE:SIMPLE
    SIZE:3
    BLUE:HUMAN
    RED:COMPUTER
    MOVES:
    BLUE,0,0,S
    RED,0,1,O
    ...
    RESULT:BLUE   or   RESULT:DRAW
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .models import GameMode, Player, Letter


@dataclass
class RecordedMove:
    player: Player
    row: int
    col: int
    letter: Letter


@dataclass
class RecordingData:
    size: int
    mode: GameMode
    blue_type: str
    red_type: str
    moves: List[RecordedMove]
    result: Optional[Player]
    is_draw: bool


class GameRecorder:
    """Handles recording a single game into a text file."""

    def __init__(self) -> None:
        self._file = None
        self.active: bool = False
        self.path: Optional[str] = None

    def start(
        self,
        path: str,
        size: int,
        mode: GameMode,
        blue_type: str,
        red_type: str,
    ) -> None:
        """Begin recording a new game to the given file path."""
        self.deactivate()  # close any existing file

        self.path = path
        self._file = open(path, "w", encoding="utf-8")
        self.active = True

        self._file.write("# SOS recording v1\n")
        self._file.write(f"MODE:{mode.name}\n")
        self._file.write(f"SIZE:{size}\n")
        self._file.write(f"BLUE:{blue_type}\n")
        self._file.write(f"RED:{red_type}\n")
        self._file.write("MOVES:\n")
        self._file.flush()

    def record_move(self, player: Player, row: int, col: int, letter: Letter) -> None:
        """Record a single move, if recording is active."""
        if not self.active or self._file is None:
            return
        self._file.write(f"{player.name},{row},{col},{letter.value}\n")
        self._file.flush()

    def finish(self, winner: Optional[Player], is_draw: bool) -> None:
        """Write the final result and close the file."""
        if not self.active or self._file is None:
            return

        if is_draw:
            self._file.write("RESULT:DRAW\n")
        elif winner is not None:
            self._file.write(f"RESULT:{winner.name}\n")
        else:
            self._file.write("RESULT:UNKNOWN\n")

        self._file.flush()
        self._file.close()
        self._file = None
        self.active = False
        self.path = None

    def deactivate(self) -> None:
        """Stop recording and close any open file without writing a result."""
        if self._file is not None:
            self._file.close()
        self._file = None
        self.active = False
        self.path = None


def load_recording(path: str) -> RecordingData:
    """Load a recorded game from a text file into a structured object."""
    mode: Optional[GameMode] = None
    size: Optional[int] = None
    blue_type = "HUMAN"
    red_type = "HUMAN"
    moves: List[RecordedMove] = []
    result_player: Optional[Player] = None
    is_draw = False

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    reading_moves = False
    for line in lines:
        if line.startswith("#"):
            continue
        if line.startswith("MODE:"):
            value = line.split(":", 1)[1].strip()
            mode = GameMode[value]
        elif line.startswith("SIZE:"):
            value = line.split(":", 1)[1].strip()
            size = int(value)
        elif line.startswith("BLUE:"):
            blue_type = line.split(":", 1)[1].strip()
        elif line.startswith("RED:"):
            red_type = line.split(":", 1)[1].strip()
        elif line.startswith("MOVES:"):
            reading_moves = True
        elif line.startswith("RESULT:"):
            reading_moves = False
            res = line.split(":", 1)[1].strip()
            if res == "DRAW":
                is_draw = True
                result_player = None
            else:
                is_draw = False
                result_player = Player[res]
        elif reading_moves:
            # Format: PLAYER,row,col,letter
            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 4:
                continue
            player_name, r_str, c_str, letter_str = parts
            player = Player[player_name]
            row = int(r_str)
            col = int(c_str)
            letter = Letter(letter_str)
            moves.append(RecordedMove(player, row, col, letter))

    if mode is None or size is None:
        raise ValueError("Recording file is missing MODE or SIZE header.")

    return RecordingData(
        size=size,
        mode=mode,
        blue_type=blue_type,
        red_type=red_type,
        moves=moves,
        result=result_player,
        is_draw=is_draw,
    )
