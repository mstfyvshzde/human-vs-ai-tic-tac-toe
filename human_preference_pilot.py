"""Experiment 2: human preference learning pilot."""

import json
import random
from pathlib import Path

from symmetric_agent import SymmetricQLearningAgent

root = Path("experiments/experiment_2/phase_2")
source = root / "models/baseline_0300.pkl"
output = root / "models/human_preference_pilot.pkl"

if output.exists():
    raise SystemExit("⚠️ Model already exists")

examples = [
    json.loads(line)
    for line in (root / "human_train.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

random.Random(42).shuffle(examples)

agent = SymmetricQLearningAgent(epsilon=0)
agent.load(str(source))

learning_rate = 0.01
margin = 0.02

updates = 0

for example in examples:
    state = (
        tuple(example["state"]["board"]),
        example["state"]["player"],
    )
    chosen = example["action"]

    legal = [
        a for a, value in enumerate(state[0])
        if value is None
    ]

    alternatives = [a for a in legal if a != chosen]
    if not alternatives:
        continue

    chosen_key = agent._key(state, chosen)

    alternative = max(
        alternatives,
        key=lambda a: agent.q_table.get(
            agent._key(state, a), 0.0
        ),
    )
    alternative_key = agent._key(state, alternative)

    chosen_q = agent.q_table.get(chosen_key, 0.0)
    other_q = agent.q_table.get(alternative_key, 0.0)

    if chosen_q < other_q + margin:
        agent.q_table[chosen_key] = chosen_q + learning_rate
        agent.q_table[alternative_key] = other_q - learning_rate
        updates += 1

agent.save(str(output))

print("=== HUMAN PREFERENCE LEARNING ===")
print("Training examples:", len(examples))
print("Preference updates:", updates)
print("Q-table entries:", len(agent.q_table))
print("Saved:", output)
print("✅ Only human choices used as preferences")
print("✅ No Minimax or hardcoded strategy")
print("✅ Baseline unchanged")
