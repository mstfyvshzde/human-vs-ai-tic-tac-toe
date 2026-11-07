from pathlib import Path


class LiveLearning:
    def __init__(self, agent, save_path="data/q_table_live.pkl"):
        self.agent = agent
        self.save_path = Path(save_path)
        self.pending = None

    def record(self, state, action):
        self.pending = (state, action)

    def observe(self, game, ai_symbol):
        if self.pending is None:
            return

        state, action = self.pending

        if game.game_over:
            if game.winner == ai_symbol:
                reward = 1.0
            elif game.winner is None:
                reward = 0.5
            else:
                reward = -1.0

            self.agent.update(
                state, action, reward, done=True
            )

        elif game.current_player == ai_symbol:
            next_state = self.agent.get_state(game)

            self.agent.update(
                state,
                action,
                reward=0.0,
                next_state=next_state,
                next_actions=game.legal_actions(),
            )

        else:
            return

        self.pending = None

    def finish(self, result):
        self.agent.save(str(self.save_path))
        self.pending = None
