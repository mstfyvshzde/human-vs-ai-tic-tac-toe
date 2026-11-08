"""Random-action control for Experiment 2 human imitation."""

import json
import random
from pathlib import Path

from symmetric_agent import SymmetricQLearningAgent

root = Path("experiments/experiment_2/phase_2")
source = root / "models/baseline_0300.pkl"
output = root / "models/random_imitation_control.pkl"

if output.exists():
    raise SystemExit("❌ Control model already exists")

examples = [
    json.loads(line)
    for line in (root / "human_train.jsonl").read_text().splitlines()
    if line.strip()
]

rng = random.Random(42)
rng.shuffle(examples)

agent = SymmetricQLearningAgent(epsilon=0)
agent.load(str(source))

learning_rate = 0.01

for example in examples:
    state = (
        tuple(example["state"]["board"]),
        example["state"]["player"],
    )

    legal = [
        i for i, value in enumerate(state[0])
        if value is None
    ]

    action = rng.choice(legal)
    key = agent._key(state, action)

    old = agent.q_table.get(key, 0.0)
    agent.q_table[key] = old + learning_rate * (1.0 - old)

agent.save(str(output))

print("=== RANDOM IMITATION CONTROL ===")
print("Examples:", len(examples))
print("Q-table entries:", len(agent.q_table))
print("Saved:", output)
print("✅ Same baseline and learning rate")
print("✅ Random legal actions only")
print("✅ No Minimax or hardcoded strategy")
print("✅ Existing models unchanged")
