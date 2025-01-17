import logging

logger = logging.getLogger(__name__)

def classify_game_state(board):
    """
    Classifies the state of the game based on the board's current configuration.
    
    Game states:
    - "opening": <= 5 moves
    - "midgame": > 5 moves without a winning condition
    - "endgame": A winning condition is met or next move decides the winner
    """
    num_moves = sum(1 for row in board for cell in row if cell != "")
    logger.debug(f"Number of moves: {num_moves}")

    if num_moves <= 5:
        logger.debug("Game state classified as 'opening'.")
        return "opening"

    if detect_win_condition(board):
        logger.debug("Game state classified as 'endgame'.")
        return "endgame"

    logger.debug("Game state classified as 'midgame'.")
    return "midgame"


def detect_win_condition(board):
    """
    Detects if there is a winning condition on the board.
    A winning condition is when 5 symbols ('X' or 'O') are in a row, column, or diagonal.
    """
    size = len(board)

    def check_line(line):
        """Check if a line contains 5 consecutive 'X' or 'O'."""
        count_x = 0
        count_o = 0
        for cell in line:
            if cell == "X":
                count_x += 1
                count_o = 0
            elif cell == "O":
                count_o += 1
                count_x = 0
            else:
                count_x = count_o = 0

            if count_x == 5 or count_o == 5:
                return True
        return False

    for i in range(size):
        if check_line(board[i]):
            return True
        if check_line([board[j][i] for j in range(size)]):
            return True

    for i in range(size):
        for j in range(size):
            if i + 4 < size and j + 4 < size:
                if check_line([board[i + k][j + k] for k in range(5)]):
                    return True
            if i + 4 < size and j - 4 >= 0:
                if check_line([board[i + k][j - k] for k in range(5)]):
                    return True

    return False
