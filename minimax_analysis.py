from functools import lru_cache

from tactical_analysis import WIN_LINES, opponent, legal_moves


def winner(board):
    for line in WIN_LINES:
        a, b, c = line
        if board[a] is not None and board[a] == board[b] == board[c]:
            return board[a]
    return None


@lru_cache(maxsize=None)
def minimax(board, player, ai_symbol):
    result = winner(board)

    if result is not None:
        return 1 if result == ai_symbol else -1

    moves = legal_moves(board)

    if not moves:
        return 0

    values = []

    for action in moves:
        next_board = list(board)
        next_board[action] = player

        value = minimax(
            tuple(next_board),
            opponent(player),
            ai_symbol
        )
        values.append(value)

    if player == ai_symbol:
        return max(values)

    return min(values)


def analyze_minimax(board, ai_symbol, chosen_action):
    moves = legal_moves(board)

    if not moves:
        return {
            "optimal_actions": [],
            "chosen_is_optimal": None,
            "chosen_value": None,
            "optimal_value": None,
            "action_values": {}
        }

    action_values = {}

    for action in moves:
        next_board = list(board)
        next_board[action] = ai_symbol

        action_values[action] = minimax(
            tuple(next_board),
            opponent(ai_symbol),
            ai_symbol
        )

    optimal_value = max(action_values.values())

    optimal_actions = [
        action for action, value in action_values.items()
        if value == optimal_value
    ]

    return {
        "optimal_actions": optimal_actions,
        "chosen_is_optimal": chosen_action in optimal_actions,
        "chosen_value": action_values.get(chosen_action),
        "optimal_value": optimal_value,
        "action_values": action_values
    }
