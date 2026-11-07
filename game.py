class TicTacToe:
    WIN_LINES = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    )

    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [None] * 9
        self.current_player = "X"
        self.winner = None
        self.winning_line = None
        self.game_over = False

    def legal_actions(self):
        if self.game_over:
            return []
        return [
            i for i, cell in enumerate(self.board)
            if cell is None
        ]

    def make_move(self, position):
        if position not in self.legal_actions():
            return False

        self.board[position] = self.current_player

        for line in self.WIN_LINES:
            if all(
                self.board[i] == self.current_player
                for i in line
            ):
                self.winner = self.current_player
                self.winning_line = line
                self.game_over = True
                return True

        if all(cell is not None for cell in self.board):
            self.game_over = True
            return True

        self.current_player = (
            "O" if self.current_player == "X" else "X"
        )
        return True
