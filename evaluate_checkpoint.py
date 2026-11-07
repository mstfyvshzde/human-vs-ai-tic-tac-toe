import json
import random
import sys
from collections import Counter
from pathlib import Path

from agent import QLearningAgent
from experiment_config import EXPERIMENT_ROOT, MODEL_FILE
from experiment_tracker import ExperimentTracker
from experiment_logger import ExperimentLogger

dataset_path = EXPERIMENT_ROOT / "evaluations" / "fixed_positions.json"
dataset = json.loads(dataset_path.read_text(encoding="utf-8"))

agent = QLearningAgent(epsilon=0.15)

if MODEL_FILE.exists():
    agent.load(str(MODEL_FILE))

# Deterministic evaluation, no exploration or learning.
random.seed(42)

counts = Counter()
total = len(dataset)

for item in dataset:
    board = item["board"]
    symbol = item["ai_symbol"]

    class Position:
        pass

    position = Position()
    position.board = board
    position.current_player = symbol

    state = agent.get_state(position)
    legal = [i for i, v in enumerate(board) if v is None]

    action, decision = agent.choose_action_tracked(
        state, legal, training=False
    )

    from tactical_analysis import analyze_tactics
    from minimax_analysis import analyze_minimax

    tactics = analyze_tactics(board, symbol, action)
    optimal = analyze_minimax(board, symbol, action)

    counts["optimal"] += bool(optimal["chosen_is_optimal"])

    for opportunity, success, prefix in [
        ("had_win_opportunity", "took_win", "win"),
        ("had_block_opportunity", "blocked", "block"),
        ("had_fork_opportunity", "created_fork", "fork"),
        ("had_fork_threat", "defended_fork", "fork_defense"),
    ]:
        if tactics[opportunity]:
            counts[prefix + "_total"] += 1
            counts[prefix + "_correct"] += bool(tactics[success])

def rate(correct, opportunities):
    if not opportunities:
        return None
    return round(100 * correct / opportunities, 2)

results = {
    "checkpoint": int(sys.argv[1]) if len(sys.argv) > 1 else 0,
    "positions": total,
    "q_table_entries": len(agent.q_table),
    "optimal_accuracy": rate(counts["optimal"], total),
}

for prefix in ("win", "block", "fork", "fork_defense"):
    results[prefix] = {
        "correct": counts[prefix + "_correct"],
        "opportunities": counts[prefix + "_total"],
        "accuracy": rate(
            counts[prefix + "_correct"],
            counts[prefix + "_total"]
        ),
    }

output = EXPERIMENT_ROOT / "evaluations" / (
    f"checkpoint_{results['checkpoint']:04d}.json"
)

if output.exists():
    raise SystemExit("❌ Checkpoint already exists; not overwritten.")

output.write_text(json.dumps(results, indent=2), encoding="utf-8")

print("=== ZERO-TO-HERO CHECKPOINT ===")
print(json.dumps(results, indent=2))
print("✅ Evaluation saved")
print("✅ AI not trained during evaluation")
