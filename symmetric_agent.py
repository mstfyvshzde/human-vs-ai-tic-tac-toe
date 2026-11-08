"""Experiment 2: symmetry-aware Q-learning."""

from agent import QLearningAgent
from symmetry import canonical_state_action


class SymmetricQLearningAgent(QLearningAgent):
    """Q-learning with canonical state-action keys."""

    def _key(self, state, action):
        return canonical_state_action(state, action)

    def choose_action(self, state, legal_actions, training=True):
        import random

        if not legal_actions:
            return None

        if training and random.random() < self.epsilon:
            return random.choice(legal_actions)

        values = {
            action: self.q_table.get(self._key(state, action), 0.0)
            for action in legal_actions
        }

        best = max(values.values())
        candidates = [
            action for action, value in values.items()
            if value == best
        ]

        return random.choice(candidates)

    def choose_action_tracked(self, state, legal_actions, training=True):
        import random

        if not legal_actions:
            return None, None

        values = {
            action: self.q_table.get(self._key(state, action), 0.0)
            for action in legal_actions
        }

        best = max(values.values())
        candidates = [
            action for action, value in values.items()
            if value == best
        ]

        exploring = training and random.random() < self.epsilon

        action = (
            random.choice(legal_actions)
            if exploring
            else random.choice(candidates)
        )

        return action, {
            "decision_type": "exploration" if exploring else "exploitation",
            "chosen_action": action,
            "legal_actions": list(legal_actions),
            "q_values": values,
            "best_actions": candidates,
            "epsilon": self.epsilon,
            "chosen_is_best_q": action in candidates,
        }

    def update(self, state, action, reward,
               next_state=None, next_actions=None, done=False):

        key = self._key(state, action)
        old = self.q_table[key]

        future = 0.0
        if not done and next_state is not None and next_actions:
            future = max(
                self.q_table[self._key(next_state, a)]
                for a in next_actions
            )

        target = reward + self.gamma * future
        self.q_table[key] = old + self.alpha * (target - old)

    def update_tracked(self, state, action, reward,
                       next_state=None, next_actions=None, done=False):

        key = self._key(state, action)
        old = self.q_table.get(key, 0.0)

        self.update(state, action, reward,
                    next_state=next_state,
                    next_actions=next_actions, done=done)

        new = self.q_table[key]
        return {
            "state": state,
            "action": action,
            "reward": reward,
            "old_q": old,
            "new_q": new,
            "delta_q": new - old,
            "alpha": self.alpha,
            "gamma": self.gamma,
            "done": done,
        }
