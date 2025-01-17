from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework import status
# -------------------------------------------------------------------
# 1) Basic Board Helpers
# -------------------------------------------------------------------

def get_empty_board() -> list[list[str]]:
    """
    Returns a 15x15 board filled with empty strings (or spaces).
    Adjust if your code uses " " instead of "".
    """
    board = []
    for _ in range(15):
        row = ["" for _ in range(15)]  # or " "
        board.append(row)
    return board


def is_15x15(board: list[list[str]]) -> bool:
    """Checks if board is exactly 15 rows of 15 columns each."""
    if len(board) != 15:
        return False
    for row in board:
        if len(row) != 15:
            return False
    return True

# -------------------------------------------------------------------
# 2) Check 5 in a Row
# -------------------------------------------------------------------

def check_five_in_a_row(board: list[list[str]]) -> bool:
    """
    Returns True if there's already a 5-in-a-row (X or O).
    """
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # down, right, diag down-right, diag up-right
    n = 15

    for r in range(n):
        for c in range(n):
            symbol = board[r][c]
            if symbol not in ["X", "O"]:
                continue  # skip empty or invalid
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < n and 0 <= cc < n and board[rr][cc] == symbol:
                    count += 1
                    rr += dr
                    cc += dc
                    if count >= 5:
                        return True
    return False

# -------------------------------------------------------------------
# 3) Can Next Move Win? (New Helper)
# -------------------------------------------------------------------

def can_next_move_win(board: list[list[str]], x_count: int, o_count: int) -> bool:
    """
    Returns True if the NEXT player to move can place a single piece
    and immediately form 5 in a row.
    """
    # Determine which player goes next:
    # If X == O, X moves next. Otherwise, O moves next.
    if x_count == o_count:
        next_player = "X"
    else:
        next_player = "O"

    n = 15
    for r in range(n):
        for c in range(n):
            if board[r][c] == "":  # or " " if you use spaces for empty
                # Place temporarily
                board[r][c] = next_player
                if check_five_in_a_row(board):
                    board[r][c] = ""  # revert
                    return True
                board[r][c] = ""  # revert
    return False

# -------------------------------------------------------------------
# 4) Main Classification
# -------------------------------------------------------------------

def classify_board(board: list[list[str]]) -> str:
    """
    Determines whether the board should be:
      - "opening"
      - "midgame"
      - "endgame"
    Raises an exception if invalid.
    """
    # 1) Check size
    if not is_15x15(board):
        raise APIException("Invalid board size", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # 2) Count symbols, check validity
    x_count, o_count = 0, 0
    for row in board:
        for cell in row:
            if cell == "X":
                x_count += 1
            elif cell == "O":
                o_count += 1
            elif cell == "":
                continue
            else:
                # Invalid symbol
                raise APIException("Invalid symbol on board", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # X must start: so x_count must be either == o_count OR x_count == o_count + 1
    if not (x_count == o_count or x_count == o_count + 1):
        raise APIException("Invalid move count", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    total_moves = x_count + o_count

    # 3) If there's already 5 in a row => 'endgame'
    if check_five_in_a_row(board):
        return "endgame"

    # 4) If next move can form 5 in a row => 'endgame'
    if can_next_move_win(board, x_count, o_count):
        return "endgame"

    # 5) If total_moves <= 5 => 'opening'
    if total_moves <= 5:
        return "opening"

    # 6) Otherwise => 'midgame'
    return "midgame"

# -------------------------------------------------------------------
# 5) High-Level Create / Update (if you do it here)
# -------------------------------------------------------------------

def create_game(payload: dict) -> dict:
    """
    Create a new game dict from payload, classify it, return the game.
    Raises 422 if invalid.
    """
    game_name = payload.get("name", "Untitled")
    difficulty = payload.get("difficulty", "easy")
    board = payload.get("board", get_empty_board())

    # Classify board
    game_state = classify_board(board)

    game = {
        "name": game_name,
        "difficulty": difficulty,
        "board": board,
        "gameState": game_state,
        "createdAt": timezone.now(),
        "updatedAt": timezone.now(),
    }
    return game


def update_game(existing_game: dict, payload: dict) -> dict:
    """
    Update existing_game in place with payload fields, re-classify, return updated game.
    """
    if "name" in payload:
        existing_game["name"] = payload["name"]
    if "difficulty" in payload:
        existing_game["difficulty"] = payload["difficulty"]
    if "board" in payload:
        existing_game["board"] = payload["board"]

    # Re-classify
    game_state = classify_board(existing_game["board"])
    existing_game["gameState"] = game_state
    existing_game["updatedAt"] = timezone.now()

    return existing_game
