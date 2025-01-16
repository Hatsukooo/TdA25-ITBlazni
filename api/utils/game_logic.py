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
    return y <= 10 and all(board[x][y + k] == symbol for k in range(5))

def check_column(board, x, y, symbol):
    return x <= 10 and all(board[x + k][y] == symbol for k in range(5))

def check_diagonal(board, x, y, symbol):
    return (
        x <= 10 and y <= 10 and all(board[x + k][y + k] == symbol for k in range(5)) or
        x >= 4 and y <= 10 and all(board[x - k][y + k] == symbol for k in range(5))
    )


def classify_game_state(board):
    logger.info(f"Classifying game state for board: {board}")
    x_count = sum(row.count('X') for row in board)
    o_count = sum(row.count('O') for row in board)

    if x_count + o_count <= 5:
        logger.info("Game state classified as 'opening'")
        return 'opening'
    
    if check_winning_condition(board, 'X') or check_winning_condition(board, 'O'):
        logger.info("Game state classified as 'endgame'")
        return 'endgame'
    
    logger.info("Game state classified as 'midgame'")
    return 'midgame'
