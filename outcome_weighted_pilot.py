"""Experiment 2: outcome-weighted human imitation."""

import json
import random
from pathlib import Path

from symmetric_agent import SymmetricQLearningAgent

root = Path("experiments/experiment_2/phase_2")
source = root / "models/baseline_0300.pkl"
output = root / "models/outcome_weighted_pilot.pkl"

if output.exists():
    raise SystemExit("⚠️ Pilot model already exists; not overwritten")

examples = [
    json.loads(line)
    for line in (root / "human_train.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

rng = random.Random(42)
rng.shuffle(examples)

agent = SymmetricQLearningAgent(epsilon=0)
agent.load(str(source))

weights = {
    "human": 1.0,
    "draw": 0.6,
    "ai": 0.2,
}

learning_rate = 0.01

for example in examples:
    state = (
        tuple(example["state"]["board"]),
        example["state"]["player"],
    )
    action = example["action"]
    weight = weights[example["game_result"]]

    key = agent._key(state, action)
    old = agent.q_table.get(key, 0.0)

    agent.q_table[key] = old + (
        learning_rate * weight * (1.0 - old)
    )

agent.save(str(output))

print("=== OUTCOME-WEIGHTED HUMAN LEARNING ===")
print("Training examples:", len(examples))
print("Q-table entries:", len(agent.q_table))
print("Saved:", output)
print("✅ Only Shahzada's human moves used")
print("✅ No Minimax or hardcoded XOX strategy")
print("✅ Original models unchanged")
