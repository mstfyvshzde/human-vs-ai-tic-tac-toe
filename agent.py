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

    def save(self, filename="data/q_table.pkl"):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("wb") as file:
            pickle.dump(dict(self.q_table), file)

    def load(self, filename="data/q_table.pkl"):
        with open(filename, "rb") as file:
            values = pickle.load(file)

        self.q_table = defaultdict(float, values)
