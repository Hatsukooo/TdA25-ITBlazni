import logging

logger = logging.getLogger(__name__)

def check_winning_condition(board, symbol):
    for i in range(15):
        for j in range(15):
            if (
                check_row(board, i, j, symbol) or
                check_column(board, i, j, symbol) or
                check_diagonal(board, i, j, symbol)
            ):
                logger.debug(f"Winning condition found at ({i}, {j}) for {symbol}")
                return True
    return False


def check_row(board, x, y, symbol):
    """Check if there is a row of five symbols starting at (x, y)."""
    if y > 10:
        return False
    return all(board[x][y + k] == symbol for k in range(5))

def check_column(board, x, y, symbol):
    """Check if there is a column of five symbols starting at (x, y)."""
    if x > 10:
        return False
    return all(board[x + k][y] == symbol for k in range(5))

def check_diagonal(board, x, y, symbol):
    """Check all diagonals starting at or overlapping (x, y)."""
    for offset in range(-4, 1):
        if 0 <= x + offset <= 10 and 0 <= y + offset <= 10:
            if all(board[x + offset + k][y + offset + k] == symbol for k in range(5)):
                return True

    for offset in range(-4, 1):
        if 4 <= x + offset <= 14 and 0 <= y + offset <= 10:
            if all(board[x + offset - k][y + offset + k] == symbol for k in range(5)):
                return True

    return False

def check_blocked_four(board, x, y, symbol):
    """Check if there is a row of four symbols that is blocked."""
    if 0 <= y <= 10:
        if (
            all(board[x][y + k] == symbol for k in range(4)) and
            (y == 0 or board[x][y - 1] != "") and
            (y + 4 >= 15 or board[x][y + 4] != "")
        ):
            return True

    if 0 <= x <= 10:
        if (
            all(board[x + k][y] == symbol for k in range(4)) and
            (x == 0 or board[x - 1][y] != "") and
            (x + 4 >= 15 or board[x + 4][y] != "")
        ):
            return True

    for offset in range(-4, 1):
        if 0 <= x + offset <= 10 and 0 <= y + offset <= 10:
            if (
                all(board[x + offset + k][y + offset + k] == symbol for k in range(4)) and
                (offset == -4 or board[x + offset - 1][y + offset - 1] != "") and
                (x + offset + 4 >= 15 or y + offset + 4 >= 15 or board[x + offset + 4][y + offset + 4] != "")
            ):
                return True

    for offset in range(-4, 1):
        if 4 <= x + offset <= 14 and 0 <= y + offset <= 10:
            if (
                all(board[x + offset - k][y + offset + k] == symbol for k in range(4)) and
                (offset == -4 or board[x + offset + 1][y + offset - 1] != "") and
                (x + offset - 4 < 0 or y + offset + 4 >= 15 or board[x + offset - 4][y + offset + 4] != "")
            ):
                return True

    return False

def classify_game_state(board):
    """Classify the game state based on the board."""
    logger.info(f"Classifying game state for board: {board}")
    x_count = sum(row.count('X') for row in board)
    o_count = sum(row.count('O') for row in board)

    # If there are very few pieces, it's the opening phase
    if x_count + o_count <= 5:
        logger.info("Game state classified as 'opening'")
        return 'opening'

    # Check for a win first
    if check_winning_condition(board, 'X'):
        logger.info("Game state classified as 'endgame' for X")
        return 'endgame'

    if check_winning_condition(board, 'O'):
        logger.info("Game state classified as 'endgame' for O")
        return 'endgame'

    # Check for blocked four
    for i in range(15):
        for j in range(15):
            if check_blocked_four(board, i, j, 'X') or check_blocked_four(board, i, j, 'O'):
                logger.info(f"Game state classified as 'midgame' due to blocked four at ({i}, {j})")
                return 'midgame'

    # Default to midgame if no other condition applies
    logger.info("Game state classified as 'midgame'")
    return 'endgame'

