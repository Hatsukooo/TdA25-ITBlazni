# app/game_logic.py

def get_empty_board() -> list[list[str]]:
    return [["" for _ in range(15)] for _ in range(15)]

def is_15x15(board: list[list[str]]) -> bool:
    if len(board) != 15:
        return False
    return all(len(row) == 15 for row in board)

def check_five_in_a_row(board: list[list[str]]) -> bool:
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    n = 15
    for r in range(n):
        for c in range(n):
            symbol = board[r][c]
            if symbol not in ["X", "O"]:
                continue
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

def can_next_move_win(board: list[list[str]], x_count: int, o_count: int) -> bool:
    next_player = "X" if x_count == o_count else "O"
    n = 15
    for r in range(n):
        for c in range(n):
            if board[r][c] == "":
                board[r][c] = next_player
                if check_five_in_a_row(board):
                    board[r][c] = ""
                    return True
                board[r][c] = ""
    return False

def classify_game_state(board: list[list[str]]) -> str:
    if not is_15x15(board):
        raise ValueError("Board must be 15x15")

    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == "X":
                x_count += 1
            elif cell == "O":
                o_count += 1
            elif cell not in ["", "X", "O"]:
                raise ValueError("Invalid symbol on board")

    if not (x_count == o_count or x_count == o_count + 1):
        raise ValueError("Invalid move count: X must start, so x_count = o_count or x_count = o_count + 1")

    if check_five_in_a_row(board):
        return "endgame"
    if can_next_move_win(board, x_count, o_count):
        return "endgame"
    total_moves = x_count + o_count
    if total_moves <= 5:
        return "opening"
    return "midgame"
