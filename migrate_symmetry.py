"""Migrate Experiment 1 Q-values into symmetry-aware representation."""

from collections import defaultdict
from pathlib import Path
import pickle
import statistics

from symmetry import canonical_state_action

SOURCE = Path(
    "experiments/experiment_2/models/initial_q_table.pkl"
)
TARGET = Path(
    "experiments/experiment_2/models/symmetric_initial.pkl"
)

if TARGET.exists():
    raise SystemExit("Target already exists; refusing to overwrite.")

# Only load our own locally generated trusted checkpoint.
with SOURCE.open("rb") as f:
    original = pickle.load(f)

groups = defaultdict(list)

for (state, action), value in original.items():
    key = canonical_state_action(state, action)
    groups[key].append(float(value))

converted = {
    key: statistics.mean(values)
    for key, values in groups.items()
}

TARGET.parent.mkdir(parents=True, exist_ok=True)

with TARGET.open("wb") as f:
    pickle.dump(converted, f)

with TARGET.open("rb") as f:
    verified = pickle.load(f)

assert verified == converted

print("Original entries:", len(original))
print("Symmetric entries:", len(converted))
print("Initial nonzero entries:", sum(v != 0 for v in converted.values()))
print("✅ Symmetry-aware initial model created")
print("✅ Original model remains unchanged")
