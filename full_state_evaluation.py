"""Experiment 2: exhaustive read-only evaluation."""

from pathlib import Path

from game import TicTacToe
from symmetry import canonical_board
from symmetric_agent import SymmetricQLearningAgent
from minimax_analysis import analyze_minimax

states = {}
visited = set()


def explore(game):
    key = (tuple(game.board), game.current_player)

    if key in visited:
        return

    visited.add(key)

    if game.game_over:
        return

    canonical = (
        canonical_board(tuple(game.board)),
        game.current_player,
    )

    states[canonical] = True

    for action in game.legal_actions():
        new = TicTacToe()
        new.board = list(game.board)
        new.current_player = game.current_player

        if not new.make_move(action):
            raise RuntimeError("Invalid move")

        explore(new)


explore(TicTacToe())

root = Path("experiments/experiment_2/phase_2/models")

models = {
    "Baseline": "baseline_0300.pkl",
    "Human Imitation": "human_imitation_pilot.pkl",
    "Human Preference": "human_preference_pilot.pkl",
    "Human Replay": "human_replay_pilot.pkl",
}

print("=== EXHAUSTIVE STATE EVALUATION ===")
print("Canonical states:", len(states))

for name, filename in models.items():
    agent = SymmetricQLearningAgent(epsilon=0)
    agent.load(str(root / filename))

    expected_optimal = 0.0
    missing_states = 0

    for board, player in states:
        state = (board, player)
        legal = [
            i for i, cell in enumerate(board)
            if cell is None
        ]

        q_values = {
            action: agent.q_table.get(
                agent._key(state, action), 0.0
            )
            for action in legal
        }

        highest = max(q_values.values())

        best_actions = [
            action for action in legal
            if q_values[action] == highest
        ]

        optimal_actions = set(
            analyze_minimax(
                board, player, best_actions[0]
            )["optimal_actions"]
        )

        expected_optimal += (
            len(set(best_actions) & optimal_actions)
            / len(best_actions)
        )

        if not any(
            agent._key(state, action) in agent.q_table
            for action in legal
        ):
            missing_states += 1

    print(f"\n{name}")
    print(
        "Expected optimal accuracy:",
        f"{100 * expected_optimal / len(states):.2f}%"
    )
    print("States without Q-table entries:", missing_states)

print("\n✅ No training")
print("✅ No model changes")
