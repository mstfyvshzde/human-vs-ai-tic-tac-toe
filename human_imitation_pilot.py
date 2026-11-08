"""Experiment 2: conservative human imitation pilot."""

import json
import random
from pathlib import Path

from symmetric_agent import SymmetricQLearningAgent
from symmetry import canonical_state_action

root = Path("experiments/experiment_2/phase_2")
source = root / "models/baseline_0300.pkl"
output = root / "models/human_imitation_pilot.pkl"

if output.exists():
    raise SystemExit("❌ Pilot model already exists")

examples = [
    json.loads(line)
    for line in (root / "human_train.jsonl").read_text().splitlines()
    if line.strip()
]

agent = SymmetricQLearningAgent(epsilon=0)
agent.load(str(source))

random.Random(42).shuffle(examples)

# Small preference adjustment, not Minimax supervision.
learning_rate = 0.01

for example in examples:
    state = (
        tuple(example["state"]["board"]),
        example["state"]["player"],
    )
    action = example["action"]

    key = canonical_state_action(state, action)

    # Encourage the demonstrated human action conservatively.
    old = agent.q_table.get(key, 0.0)
    agent.q_table[key] = old + learning_rate * (1.0 - old)

agent.save(str(output))

print("=== LEARNING FROM SHAHZADA ===")
print("Training examples:", len(examples))
print("Q-table entries:", len(agent.q_table))
print("Saved:", output)
print("✅ Only human training data used")
print("✅ No Minimax or hardcoded strategy")
print("✅ Baseline model unchanged")
