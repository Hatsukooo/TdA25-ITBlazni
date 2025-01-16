import logging
logger = logging.getLogger(__name__)

def check_winning_condition(board, symbol):
    """Check if the given symbol has five in a row."""
    for i in range(15):
        for j in range(15):
            if (
                check_row(board, i, j, symbol) or
                check_column(board, i, j, symbol) or
                check_diagonal(board, i, j, symbol)
            ):
                return True
    return False

def check_row(board, x, y, symbol):
    """Check if there is a row of five symbols starting at (x, y)."""
    if y > 10:  # Prevent overflow
        return False
    return all(board[x][y + k] == symbol for k in range(5))

def check_column(board, x, y, symbol):
    """Check if there is a column of five symbols starting at (x, y)."""
    if x > 10:  # Prevent overflow
        return False
    return all(board[x + k][y] == symbol for k in range(5))

def check_diagonal(board, x, y, symbol):
    """Check if there is a diagonal of five symbols starting at (x, y)."""
    # Top-left to bottom-right
    if x <= 10 and y <= 10 and all(board[x + k][y + k] == symbol for k in range(5)):
        return True
    # Bottom-left to top-right
    if x >= 4 and y <= 10 and all(board[x - k][y + k] == symbol for k in range(5)):
        return True
    return False

def check_blocked_four(board, x, y, symbol):
    """Check if there is a row of four symbols that is blocked."""
    # Add logic for blocked rows, columns, and diagonals
    # For simplicity, assume blocked means any obstruction at both ends
    if y >= 1 and y <= 10:  # Ensure room for a block
        if (
            all(board[x][y + k] == symbol for k in range(4)) and
            board[x][y - 1] != "" and board[x][y + 4] != ""
        ):
            return True
    if x >= 1 and x <= 10:  # Vertical block
        if (
            all(board[x + k][y] == symbol for k in range(4)) and
            board[x - 1][y] != "" and board[x + 4][y] != ""
        ):
            return True
    # Check diagonal blocks (both directions)...
    return False

def classify_game_state(board):
    """Classify the game state based on the board."""
    logger.info(f"Classifying game state for board: {board}")
    x_count = sum(row.count('X') for row in board)
    o_count = sum(row.count('O') for row in board)

    if x_count + o_count <= 5:
        logger.info("Game state classified as 'opening'")
        return 'opening'

    if check_winning_condition(board, 'X'):
        logger.info("Game state classified as 'endgame' for X")
        return 'endgame'

    if check_winning_condition(board, 'O'):
        logger.info("Game state classified as 'endgame' for O")
        return 'endgame'

    for i in range(15):
        for j in range(15):
            if check_blocked_four(board, i, j, 'X') or check_blocked_four(board, i, j, 'O'):
                logger.info(f"Game state classified as 'midgame' due to blocked four at ({i}, {j})")
                return 'midgame'

    logger.info("Game state classified as 'midgame'")
    return 'midgame'

