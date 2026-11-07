import random
import pickle
from pathlib import Path
from collections import defaultdict


class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.95, epsilon=0.2):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = defaultdict(float)

    def get_state(self, game):
        return (tuple(game.board), game.current_player)

    def choose_action(self, state, legal_actions, training=True):
        if not legal_actions:
            return None

        if training and random.random() < self.epsilon:
            return random.choice(legal_actions)

        values = [
            self.q_table[(state, action)]
            for action in legal_actions
        ]

        best_value = max(values)
        best_actions = [
            action for action, value in zip(legal_actions, values)
            if value == best_value
        ]

        return random.choice(best_actions)


    def choose_action_tracked(self, state, legal_actions, training=True):
        if not legal_actions:
            return None, None

        import random

        q_values = {
            action: self.q_table.get((state, action), 0.0)
            for action in legal_actions
        }

        best_value = max(q_values.values())
        best_actions = [
            action for action in legal_actions
            if q_values[action] == best_value
        ]

        exploring = training and random.random() < self.epsilon

        if exploring:
            action = random.choice(legal_actions)
        else:
            action = random.choice(best_actions)

        details = {
            "decision_type": "exploration" if exploring else "exploitation",
            "chosen_action": action,
            "legal_actions": list(legal_actions),
            "q_values": q_values,
            "best_actions": best_actions,
            "epsilon": self.epsilon,
            "chosen_is_best_q": action in best_actions,
        }

        return action, details

    def update(self, state, action, reward,
               next_state=None, next_actions=None, done=False):

        old_value = self.q_table[(state, action)]

        if done or not next_actions:
            future_value = 0.0
        else:
            future_value = max(
                self.q_table[(next_state, a)]
                for a in next_actions
            )

        target = reward + self.gamma * future_value

        self.q_table[(state, action)] = (
            old_value
            + self.alpha * (target - old_value)
        )


    def update_tracked(
        self, state, action, reward,
        next_state=None, next_actions=None, done=False
    ):
        old_value = self.q_table.get((state, action), 0.0)

        self.update(
            state,
            action,
            reward,
            next_state=next_state,
            next_actions=next_actions,
            done=done
        )

        new_value = self.q_table[(state, action)]

        return {
            "state": state,
            "action": action,
            "reward": reward,
            "old_q": old_value,
            "new_q": new_value,
            "delta_q": new_value - old_value,
            "alpha": self.alpha,
            "gamma": self.gamma,
            "done": done
        }

    def save(self, filename="data/q_table.pkl"):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("wb") as file:
            pickle.dump(dict(self.q_table), file)

    def load(self, filename="data/q_table.pkl"):
        with open(filename, "rb") as file:
            values = pickle.load(file)

        self.q_table = defaultdict(float, values)
