"""Step definitions for Chinese Chess scenarios"""

import re

from behave import given, then, when

from src.chess_service import ChessService


def parse_position(position_str: str):
    """Parse position string like '(1, 5)' into (row, col) tuple"""
    match = re.match(r"\((\d+),\s*(\d+)\)", position_str)
    if match:
        return (int(match.group(1)), int(match.group(2)))
    raise ValueError(f"Invalid position format: {position_str}")


@given("the board is empty except for a {color} {piece_type} at {position}")
def step_board_with_single_piece(context, color, piece_type, position):
    """Initialize board with only one piece at specified position"""
    context.service = ChessService()
    context.service.set_empty_board()

    # Parse position
    row, col = parse_position(position)

    # Add piece to board
    context.service.add_piece_to_board(piece_type, color, row, col)

    # Store initial position for reference
    context.last_move_legal = None


@given("the board has:")
def step_board_with_pieces(context):
    """Initialize board with pieces from a data table"""
    context.service = ChessService()
    context.service.set_empty_board()

    for row in context.table:
        # Parse piece description like "Red General"
        piece_info = row["Piece"].split()
        color = piece_info[0]
        piece_type = " ".join(piece_info[1:])

        # Parse position
        position = row["Position"]
        pos_row, pos_col = parse_position(position)

        # Add piece to board
        context.service.add_piece_to_board(piece_type, color, pos_row, pos_col)

    context.last_move_legal = None


@when("Red moves the {piece_type} from {from_pos} to {to_pos}")
def step_red_moves_piece(context, piece_type, from_pos, to_pos):
    """Execute a move for the Red piece"""
    from_row, from_col = parse_position(from_pos)
    to_row, to_col = parse_position(to_pos)

    # Check if move is valid
    context.last_move_legal = context.service.is_valid_move(
        from_row, from_col, to_row, to_col
    )

    # Execute the move if valid
    if context.last_move_legal:
        context.service.execute_move(from_row, from_col, to_row, to_col)

    # Store move info for later assertions
    context.last_move = {
        "from": (from_row, from_col),
        "to": (to_row, to_col),
        "piece_type": piece_type,
    }


@then("the move is legal")
def step_move_is_legal(context):
    """Assert that the move is legal"""
    assert context.last_move_legal is True, "Expected move to be legal, but it was not"


@then("the move is illegal")
def step_move_is_illegal(context):
    """Assert that the move is illegal"""
    assert context.last_move_legal is False, (
        "Expected move to be illegal, but it was legal"
    )


@then("Red wins immediately")
def step_red_wins_immediately(context):
    """Assert that Red wins immediately"""
    assert context.service.is_game_over() is True, "Expected game to be over (Red wins)"


@then("the game is not over just from that capture")
def step_game_continues(context):
    """Assert that the game continues after capture"""
    assert context.service.is_game_over() is False, (
        "Expected game to continue after capture"
    )
