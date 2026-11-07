from pathlib import Path


class LiveLearning:
    def __init__(self, agent, save_path="data/q_table_live.pkl", logger=None):
        self.agent = agent
        self.logger = logger
        self.game_id = None
        self.move_number = None
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

            self._apply_update(
                state, action, reward, done=True
            )

        elif game.current_player == ai_symbol:
            next_state = self.agent.get_state(game)

            self._apply_update(
                state,
                action,
                reward=0.0,
                next_state=next_state,
                next_actions=game.legal_actions(),
            )

        else:
            return

        self.pending = None


    def _apply_update(self, *args, **kwargs):
        if self.logger is None:
            return self.agent.update(*args, **kwargs)

        details = self.agent.update_tracked(*args, **kwargs)
        self.logger.log_learning(
            game_id=self.game_id,
            move_number=self.move_number,
            **details
        )
        return details

    def finish(self, result):
        self.agent.save(str(self.save_path))
        self.pending = None
