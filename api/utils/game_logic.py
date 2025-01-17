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

    if detect_win_condition(board, check_potential=True):
        logger.debug("Game state classified as 'endgame'.")
        return "endgame"

    logger.debug("Game state classified as 'midgame'.")
    return "midgame"

def detect_win_condition(board, check_potential=False):
    """
    Detects if there is a winning condition on the board.
    If `check_potential` is True, also checks for potential winning moves.

    Winning condition: 5 symbols ('X' or 'O') in a row, column, or diagonal.
    Potential condition: 4 consecutive symbols with at least one open end.
    """
    size = len(board)

    def check_line(line):
        """Check if a line contains 5 consecutive 'X' or 'O' or a potential win."""
        count_x = 0
        count_o = 0
        for i, cell in enumerate(line):
            if cell == "X":
                count_x += 1
                count_o = 0
            elif cell == "O":
                count_o += 1
                count_x = 0
            else:
                if check_potential:
                    if count_x == 4 or count_o == 4:
                        if i > 0 and i < len(line):
                            if (line[i - 1] == "" or line[i] == ""):
                                return "potential"
                count_x = count_o = 0

            if count_x == 5 or count_o == 5:
                return "win"
        return "none"

    for i in range(size):
        if check_line(board[i]) == "win" or check_line([board[j][i] for j in range(size)]) == "win":
            return True

        if check_potential:
            if check_line(board[i]) == "potential" or check_line([board[j][i] for j in range(size)]) == "potential":
                return True

    for i in range(size):
        for j in range(size):
            if i + 4 < size and j + 4 < size:
                major_diag = [board[i + k][j + k] for k in range(5)]
                if check_line(major_diag) == "win":
                    return True
                if check_potential and check_line(major_diag) == "potential":
                    return True

            if i + 4 < size and j - 4 >= 0:
                minor_diag = [board[i + k][j - k] for k in range(5)]
                if check_line(minor_diag) == "win":
                    return True
                if check_potential and check_line(minor_diag) == "potential":
                    return True

    return False