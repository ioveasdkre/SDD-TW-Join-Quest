"""Chinese Chess domain models"""

from enum import Enum
from typing import Optional, Tuple


class Color(Enum):
    """Chess piece color"""

    RED = "Red"
    BLACK = "Black"


class PieceType(Enum):
    """Chinese Chess piece types"""

    GENERAL = "General"  # 將/帥
    GUARD = "Guard"  # 士/仕
    ELEPHANT = "Elephant"  # 象/相
    HORSE = "Horse"  # 馬/傌
    ROOK = "Rook"  # 車
    CANNON = "Cannon"  # 炮
    SOLDIER = "Soldier"  # 兵/卒


class Piece:
    """Represents a chess piece"""

    def __init__(self, piece_type: PieceType, color: Color):
        self.type = piece_type
        self.color = color

    def __repr__(self):
        return f"{self.color.value} {self.type.value}"


class Board:
    """Represents the 9×10 Chinese Chess board"""

    def __init__(self):
        """Initialize an empty board"""
        # Board is 9 columns × 10 rows
        # Stored as (row, col) where row 1-10, col 1-9
        self.pieces = {}  # (row, col) -> Piece

    def set_piece(self, row: int, col: int, piece: Piece) -> None:
        """Place a piece on the board"""
        if self.is_within_bounds(row, col):
            self.pieces[(row, col)] = piece

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """Get piece at position, returns None if empty"""
        return self.pieces.get((row, col))

    def clear_position(self, row: int, col: int) -> None:
        """Remove piece from position"""
        if (row, col) in self.pieces:
            del self.pieces[(row, col)]

    def is_empty(self, row: int, col: int) -> bool:
        """Check if a position is empty"""
        return (row, col) not in self.pieces

    def is_within_bounds(self, row: int, col: int) -> bool:
        """Check if position is within board boundaries"""
        return 1 <= row <= 10 and 1 <= col <= 9


class Move:
    """Represents a chess move"""

    def __init__(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]):
        self.from_pos = from_pos
        self.to_pos = to_pos


class GameState:
    """Represents the current game state"""

    def __init__(self):
        self.board = Board()
        self.last_move = None
