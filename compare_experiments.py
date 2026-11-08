"""Compare Experiment 1 and Experiment 2 without training."""

import json
import random
from pathlib import Path

from agent import QLearningAgent
from symmetric_agent import SymmetricQLearningAgent
from minimax_analysis import analyze_minimax
from tactical_analysis import analyze_tactics

ROOT = Path("experiments")
dataset = json.loads(
    (ROOT / "zero_to_hero_2/evaluations/fixed_positions.json")
    .read_text(encoding="utf-8")
)

models = {
    "Experiment 1": (
        QLearningAgent(epsilon=0),
        ROOT / "experiment_2/models/initial_q_table.pkl",
    ),
    "Experiment 2": (
        SymmetricQLearningAgent(epsilon=0),
        ROOT / "experiment_2/models/symmetric_initial.pkl",
    ),
}


def evaluate(agent):
    # Random seed is controlled by the caller.

    counts = {
        "optimal": 0,
        "block_correct": 0,
        "block_total": 0,
        "win_correct": 0,
        "win_total": 0,
    }

    for item in dataset:
        board = item["board"]
        symbol = item["ai_symbol"]
        state = (tuple(board), symbol)

        legal = [
            i for i, value in enumerate(board)
            if value is None
        ]

        action = agent.choose_action(
            state, legal, training=False
        )

        optimal = analyze_minimax(board, symbol, action)
        tactics = analyze_tactics(board, symbol, action)

        counts["optimal"] += bool(
            optimal["chosen_is_optimal"]
        )

        if tactics["had_block_opportunity"]:
            counts["block_total"] += 1
            counts["block_correct"] += bool(
                tactics["blocked"]
            )

        if tactics["had_win_opportunity"]:
            counts["win_total"] += 1
            counts["win_correct"] += bool(
                tactics["took_win"]
            )

    return counts


for name, (agent, path) in models.items():
    agent.load(str(path))
    counts = evaluate(agent)

    optimal = 100 * counts["optimal"] / len(dataset)

    block = (
        100 * counts["block_correct"] / counts["block_total"]
        if counts["block_total"] else 0
    )

    win = (
        100 * counts["win_correct"] / counts["win_total"]
        if counts["win_total"] else 0
    )

    print(f"\n=== {name} ===")
    print(f"Optimal moves: {optimal:.2f}%")
    print(f"Correct blocks: {block:.2f}%")
    print(f"Winning moves: {win:.2f}%")
    print(f"Q-table entries: {len(agent.q_table)}")

print("\n✅ No training performed")
print("✅ No model files modified")
