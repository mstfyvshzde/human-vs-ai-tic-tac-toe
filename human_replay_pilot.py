"""Experiment 2: offline Q-learning from real human games."""

import json
from pathlib import Path
from collections import Counter

from symmetric_agent import SymmetricQLearningAgent

root = Path("experiments/experiment_2")
phase = root / "phase_2"

source = phase / "models/baseline_0300.pkl"
output = phase / "models/human_replay_pilot.pkl"

if output.exists():
    raise SystemExit("⚠️ Replay model already exists")

with (phase / "human_train.jsonl").open(encoding="utf-8") as f:
    examples = [json.loads(line) for line in f if line.strip()]

train_games = sorted({x["game_id"] for x in examples})
expected = Counter(x["game_id"] for x in examples)

agent = SymmetricQLearningAgent(
    alpha=0.1,
    gamma=0.95,
    epsilon=0,
)
agent.load(str(source))

updates = 0
rewards = Counter()

for game_id in train_games:
    path = root / "games" / f"game_{game_id:04d}.json"
    game = json.loads(path.read_text(encoding="utf-8"))

    symbol = game["summary"]["human_symbol"]
    winner = game["summary"]["winner"]

    human_moves = [
        m for m in game["moves"]
        if m["player"] == "human"
    ]

    if len(human_moves) != expected[game_id]:
        raise RuntimeError(f"Mismatch in game {game_id}")

    for i, move in enumerate(human_moves):
        state = (tuple(move["board_before"]), symbol)
        action = move["action"]

        if state[0][action] is not None:
            raise RuntimeError(f"Illegal action in game {game_id}")

        if i + 1 < len(human_moves):
            following = human_moves[i + 1]
            next_board = tuple(following["board_before"])
            next_state = (next_board, symbol)
            legal = [
                a for a, cell in enumerate(next_board)
                if cell is None
            ]

            agent.update(
                state, action,
                reward=0.0,
                next_state=next_state,
                next_actions=legal,
                done=False,
            )
        else:
            reward = {
                "human": 1.0,
                "draw": 0.5,
                "ai": -1.0,
            }[winner]

            agent.update(
                state, action,
                reward=reward,
                done=True,
            )
            rewards[winner] += 1

        updates += 1

assert updates == len(examples)
assert sum(rewards.values()) == len(train_games)

agent.save(str(output))

print("=== HUMAN EXPERIENCE REPLAY ===")
print("Training games:", len(train_games))
print("Human moves updated:", updates)
print("Terminal rewards:", dict(rewards))
print("Q-table entries:", len(agent.q_table))
print("Saved:", output)
print("✅ Only training games used")
print("✅ No Minimax supervision")
print("✅ Baseline unchanged")
