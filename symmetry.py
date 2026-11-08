"""Board symmetry utilities for Experiment 2.

Board positions use indices 0..8.
No game strategy or preferred moves are encoded here.
"""

def transform_index(index, rotation=0, reflect=False):
    row, col = divmod(index, 3)

    if reflect:
        col = 2 - col

    for _ in range(rotation % 4):
        row, col = col, 2 - row

    return row * 3 + col


def transform_board(board, rotation=0, reflect=False):
    if len(board) != 9:
        raise ValueError("Board must contain exactly 9 cells")

    result = [None] * 9

    for old_index, value in enumerate(board):
        new_index = transform_index(
            old_index, rotation, reflect
        )
        result[new_index] = value

    return tuple(result)


def canonical_board(board):
    """Return the same representation for equivalent boards."""
    variants = [
        transform_board(board, rotation, reflect)
        for reflect in (False, True)
        for rotation in range(4)
    ]

    return min(
        variants,
        key=lambda b: tuple(str(v) for v in b)
    )


def canonical_state_action(state, action):
    """Canonicalize a (state, action) pair under all 8 symmetries.

    This does not assign rewards or choose optimal moves.
    """
    board, player = state

    if len(board) != 9:
        raise ValueError("Board must contain exactly 9 cells")

    if not isinstance(action, int) or not 0 <= action < 9:
        raise ValueError("Action must be an index from 0 to 8")

    variants = []

    for reflect in (False, True):
        for rotation in range(4):
            new_board = transform_board(
                board, rotation, reflect
            )
            new_action = transform_index(
                action, rotation, reflect
            )

            variants.append((new_board, new_action))

    board_key, action_key = min(
        variants,
        key=lambda item: (
            tuple(str(cell) for cell in item[0]),
            item[1],
        ),
    )

    return ((board_key, player), action_key)
