WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def opponent(symbol):
    return "O" if symbol == "X" else "X"


def legal_moves(board):
    return [i for i, cell in enumerate(board) if cell is None]


def winning_moves(board, symbol):
    result = []

    for action in legal_moves(board):
        test = list(board)
        test[action] = symbol

        if any(
            all(test[i] == symbol for i in line)
            for line in WIN_LINES
        ):
            result.append(action)

    return result


def fork_moves(board, symbol):
    result = []

    for action in legal_moves(board):
        test = list(board)
        test[action] = symbol

        if len(winning_moves(test, symbol)) >= 2:
            result.append(action)

    return result


def analyze_tactics(board, ai_symbol, chosen_action):
    human_symbol = opponent(ai_symbol)

    wins = winning_moves(board, ai_symbol)
    threats = winning_moves(board, human_symbol)
    forks = fork_moves(board, ai_symbol)
    human_forks = fork_moves(board, human_symbol)

    # Test possible defenses by simulating an AI action
    fork_defenses = []
    for action in legal_moves(board):
        test = list(board)
        test[action] = ai_symbol

        if not fork_moves(test, human_symbol):
            fork_defenses.append(action)

    return {
        "ai_winning_moves": wins,
        "human_winning_threats": threats,
        "ai_fork_moves": forks,
        "human_fork_threats": human_forks,
        "fork_defenses": fork_defenses,
        "had_win_opportunity": bool(wins),
        "took_win": chosen_action in wins,
        "had_block_opportunity": bool(threats) and not wins,
        "blocked": chosen_action in threats if threats and not wins else None,
        "had_fork_opportunity": bool(forks),
        "created_fork": chosen_action in forks,
        "had_fork_threat": bool(human_forks),
        "defended_fork": chosen_action in fork_defenses if human_forks else None
    }
