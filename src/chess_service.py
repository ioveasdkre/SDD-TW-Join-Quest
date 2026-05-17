"""Chinese Chess Service module"""

from src.chess_models import Color, GameState, Piece, PieceType


class ChessService:
    """Service for managing Chinese Chess game logic"""

    def __init__(self):
        """Initialize the chess service"""
        self.game_state = GameState()

    def set_empty_board(self) -> None:
        """Reset board to empty state"""
        self.game_state = GameState()

    def add_piece_to_board(
        self, piece_type_str: str, color_str: str, row: int, col: int
    ) -> None:
        """Add a piece to the board at specified position"""
        # Convert string representations to enums
        piece_type = PieceType[piece_type_str.upper()]
        color = Color[color_str.upper()]
        piece = Piece(piece_type, color)
        self.game_state.board.set_piece(row, col, piece)

    def is_valid_move(
        self, from_row: int, from_col: int, to_row: int, to_col: int
    ) -> bool:
        """Check if a move is valid according to chess rules"""
        # Check if positions are within bounds
        if not self.game_state.board.is_within_bounds(from_row, from_col):
            return False
        if not self.game_state.board.is_within_bounds(to_row, to_col):
            return False

        # Check if source has a piece
        piece = self.game_state.board.get_piece(from_row, from_col)
        if piece is None:
            return False

        # Route to specific piece type validation
        if piece.type == PieceType.GENERAL:
            return self._is_valid_general_move(
                piece.color, from_row, from_col, to_row, to_col
            )
        elif piece.type == PieceType.GUARD:
            return self._is_valid_guard_move(
                piece.color, from_row, from_col, to_row, to_col
            )
        elif piece.type == PieceType.ELEPHANT:
            return self._is_valid_elephant_move(
                piece.color, from_row, from_col, to_row, to_col
            )
        elif piece.type == PieceType.HORSE:
            return self._is_valid_horse_move(
                piece.color, from_row, from_col, to_row, to_col
            )
        elif piece.type == PieceType.ROOK:
            return self._is_valid_rook_move(
                piece.color, from_row, from_col, to_row, to_col
            )
        elif piece.type == PieceType.CANNON:
            return self._is_valid_cannon_move(
                piece.color, from_row, from_col, to_row, to_col
            )
        elif piece.type == PieceType.SOLDIER:
            return self._is_valid_soldier_move(
                piece.color, from_row, from_col, to_row, to_col
            )

        return False

    def _is_valid_general_move(
        self, color: Color, from_row: int, from_col: int, to_row: int, to_col: int
    ) -> bool:
        """Validate General (將/帥) move"""
        # Define palace boundaries for each side
        # Red palace: rows 1-3, cols 4-6
        # Black palace: rows 8-10, cols 4-6
        if color == Color.RED:
            palace_rows = (1, 3)
            palace_cols = (4, 6)
        else:  # BLACK
            palace_rows = (8, 10)
            palace_cols = (4, 6)

        # Check if from and to positions are within palace
        if not (
            palace_rows[0] <= from_row <= palace_rows[1]
            and palace_cols[0] <= from_col <= palace_cols[1]
        ):
            return False

        if not (
            palace_rows[0] <= to_row <= palace_rows[1]
            and palace_cols[0] <= to_col <= palace_cols[1]
        ):
            return False

        # Check if it's a one-step move (adjacent)
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        # Valid moves: one step horizontally or vertically, not diagonally
        if (row_diff + col_diff) != 1:
            return False

        # Check if target position has a same-colored piece
        target_piece = self.game_state.board.get_piece(to_row, to_col)
        if target_piece is not None and target_piece.color == color:
            return False

        # Check if generals are facing each other (flying general rule)
        if not self._are_generals_facing(color, to_row, to_col):
            return False

        return True

    def _are_generals_facing(
        self, color: Color, new_general_row: int, new_general_col: int
    ) -> bool:
        """Check if generals are facing each other after move"""
        # Find the other general
        opponent_color = Color.BLACK if color == Color.RED else Color.RED
        opponent_general_pos = None

        for pos, piece in self.game_state.board.pieces.items():
            if piece.type == PieceType.GENERAL and piece.color == opponent_color:
                opponent_general_pos = pos
                break

        if opponent_general_pos is None:
            return True  # No opponent general yet

        # Check if they are on the same column with no pieces between them
        if new_general_col != opponent_general_pos[1]:
            return True  # Not on same column

        # Check if they are facing each other (same column, opposite sides)
        min_row = min(new_general_row, opponent_general_pos[0])
        max_row = max(new_general_row, opponent_general_pos[0])

        # Check for pieces between them
        for row in range(min_row + 1, max_row):
            if not self.game_state.board.is_empty(row, new_general_col):
                return True  # There's a piece between them

        # They are facing each other with no piece between - illegal
        return False

    def _is_valid_guard_move(
        self, color: Color, from_row: int, from_col: int, to_row: int, to_col: int
    ) -> bool:
        """Validate Guard (士/仕) move"""
        # Define palace boundaries for each side
        if color == Color.RED:
            palace_rows = (1, 3)
            palace_cols = (4, 6)
        else:  # BLACK
            palace_rows = (8, 10)
            palace_cols = (4, 6)

        # Check if from and to positions are within palace
        if not (
            palace_rows[0] <= from_row <= palace_rows[1]
            and palace_cols[0] <= from_col <= palace_cols[1]
        ):
            return False

        if not (
            palace_rows[0] <= to_row <= palace_rows[1]
            and palace_cols[0] <= to_col <= palace_cols[1]
        ):
            return False

        # Guard moves diagonally one step
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        # Must move diagonally exactly one step
        if row_diff != 1 or col_diff != 1:
            return False

        # Check if target position has a same-colored piece
        target_piece = self.game_state.board.get_piece(to_row, to_col)
        if target_piece is not None and target_piece.color == color:
            return False

        return True

    def _is_valid_elephant_move(
        self, color: Color, from_row: int, from_col: int, to_row: int, to_col: int
    ) -> bool:
        """Validate Elephant (象/相) move"""
        # Elephant moves diagonally 2 steps
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        # Must move diagonally exactly 2 steps
        if row_diff != 2 or col_diff != 2:
            return False

        # Check river constraint
        # Red elephant: rows 1-5 only
        # Black elephant: rows 6-10 only
        if color == Color.RED:
            if from_row > 5 or to_row > 5:
                return False
        else:  # BLACK
            if from_row < 6 or to_row < 6:
                return False

        # Check if midpoint is blocked
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        if not self.game_state.board.is_empty(mid_row, mid_col):
            return False

        # Check if target position has a same-colored piece
        target_piece = self.game_state.board.get_piece(to_row, to_col)
        if target_piece is not None and target_piece.color == color:
            return False

        return True

    def _is_valid_horse_move(
        self, color: Color, from_row: int, from_col: int, to_row: int, to_col: int
    ) -> bool:
        """Validate Horse (馬/傌) move"""
        # Horse moves in an L-shape: 2 squares in one direction, 1 square perpendicular
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        # Valid L-shape moves
        is_valid_shape = (row_diff == 2 and col_diff == 1) or (
            row_diff == 1 and col_diff == 2
        )
        if not is_valid_shape:
            return False

        # Check if the "leg" is blocked
        # The leg is the first square in the longer direction
        if row_diff == 2:
            # Vertical L-shape (2 rows, 1 col)
            leg_row = from_row + (1 if to_row > from_row else -1)
            leg_col = from_col
        else:
            # Horizontal L-shape (1 row, 2 cols)
            leg_row = from_row
            leg_col = from_col + (1 if to_col > from_col else -1)

        # Check if leg is blocked
        if not self.game_state.board.is_empty(leg_row, leg_col):
            return False

        # Check if target position has a same-colored piece
        target_piece = self.game_state.board.get_piece(to_row, to_col)
        if target_piece is not None and target_piece.color == color:
            return False

        return True

    def _is_valid_rook_move(
        self, color: Color, from_row: int, from_col: int, to_row: int, to_col: int
    ) -> bool:
        """Validate Rook (車) move"""
        # Rook moves horizontally or vertically any number of squares,
        # but cannot jump over pieces

        # Must move horizontally OR vertically, not both
        if from_row != to_row and from_col != to_col:
            return False

        # Cannot move to the same position
        if from_row == to_row and from_col == to_col:
            return False

        # Check if path is clear
        if from_row == to_row:
            # Horizontal movement
            start_col = min(from_col, to_col)
            end_col = max(from_col, to_col)
            for col in range(start_col + 1, end_col):
                if not self.game_state.board.is_empty(from_row, col):
                    return False  # Path blocked
        else:
            # Vertical movement
            start_row = min(from_row, to_row)
            end_row = max(from_row, to_row)
            for row in range(start_row + 1, end_row):
                if not self.game_state.board.is_empty(row, from_col):
                    return False  # Path blocked

        # Check if target position has a same-colored piece
        target_piece = self.game_state.board.get_piece(to_row, to_col)
        if target_piece is not None and target_piece.color == color:
            return False

        return True

    def _is_valid_cannon_move(
        self, color: Color, from_row: int, from_col: int, to_row: int, to_col: int
    ) -> bool:
        """Validate Cannon (炮) move"""
        # Cannon moves like a Rook horizontally or vertically
        # But has two modes:
        # 1. Normal move: like a Rook with clear path
        # 2. Capture move: must jump over exactly one piece to capture

        # Must move horizontally OR vertically, not both
        if from_row != to_row and from_col != to_col:
            return False

        # Cannot move to the same position
        if from_row == to_row and from_col == to_col:
            return False

        # Count pieces in the path
        pieces_in_path = []
        if from_row == to_row:
            # Horizontal movement
            start_col = min(from_col, to_col)
            end_col = max(from_col, to_col)
            for col in range(start_col + 1, end_col):
                if not self.game_state.board.is_empty(from_row, col):
                    pieces_in_path.append((from_row, col))
        else:
            # Vertical movement
            start_row = min(from_row, to_row)
            end_row = max(from_row, to_row)
            for row in range(start_row + 1, end_row):
                if not self.game_state.board.is_empty(row, from_col):
                    pieces_in_path.append((row, from_col))

        target_piece = self.game_state.board.get_piece(to_row, to_col)

        if target_piece is None:
            # Normal move: no target, must have clear path
            if len(pieces_in_path) > 0:
                return False
        else:
            # Capture move: must jump over exactly one piece
            if len(pieces_in_path) != 1:
                return False
            # Cannot capture same-colored piece
            if target_piece.color == color:
                return False

        return True

    def _is_valid_soldier_move(
        self, color: Color, from_row: int, from_col: int, to_row: int, to_col: int
    ) -> bool:
        """Validate Soldier (兵/卒) move"""
        # Soldier moves one square at a time
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        # Must move exactly one square
        if (row_diff + col_diff) != 1:
            return False

        # Check if target position has a same-colored piece
        target_piece = self.game_state.board.get_piece(to_row, to_col)
        if target_piece is not None and target_piece.color == color:
            return False

        # Check movement constraints based on river crossing
        if color == Color.RED:
            # Red moves "forward" meaning row increases
            if from_row <= 5:
                # Before crossing river: only forward movement (row increases)
                if to_row != from_row + 1:
                    return False
            else:
                # After crossing river: forward (row increases) or sideways (col changes)
                # Cannot move backward (row decreases)
                if to_row < from_row:
                    return False
        else:
            # Black moves "forward" meaning row decreases
            if from_row >= 6:
                # Before crossing river: only forward movement (row decreases)
                if to_row != from_row - 1:
                    return False
            else:
                # After crossing river: forward (row decreases) or sideways (col changes)
                # Cannot move backward (row increases)
                if to_row > from_row:
                    return False

        return True

    def execute_move(
        self, from_row: int, from_col: int, to_row: int, to_col: int
    ) -> bool:
        """Execute a move on the board"""
        if not self.is_valid_move(from_row, from_col, to_row, to_col):
            return False

        # Move piece
        piece = self.game_state.board.get_piece(from_row, from_col)
        self.game_state.board.clear_position(from_row, from_col)
        self.game_state.board.set_piece(to_row, to_col, piece)

        return True

    def is_game_over(self) -> bool:
        """Check if game is over (one general captured)"""
        red_general_exists = False
        black_general_exists = False

        for pos, piece in self.game_state.board.pieces.items():
            if piece.type == PieceType.GENERAL:
                if piece.color == Color.RED:
                    red_general_exists = True
                else:
                    black_general_exists = True

        return not (red_general_exists and black_general_exists)
