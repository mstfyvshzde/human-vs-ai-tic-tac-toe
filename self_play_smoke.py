"""Experiment 2 Phase 2: isolated 10-game self-play test."""

import hashlib
import json
import random
from collections import Counter
from pathlib import Path

from game import TicTacToe
from symmetric_agent import SymmetricQLearningAgent

random.seed(42)

root = Path("experiments/experiment_2/phase_2")
source = root / "models/baseline_0300.pkl"
output = root / "smoke_test"

if not source.is_file():
    raise SystemExit("❌ Phase 2 baseline not found")

if output.exists():
    raise SystemExit("❌ Smoke test folder already exists; nothing overwritten")

baseline_hash = hashlib.sha256(source.read_bytes()).hexdigest()

agent = SymmetricQLearningAgent(
    alpha=0.1,
    gamma=0.95,
    epsilon=0.15,
)
agent.load(str(source))

output.mkdir(parents=True)
games_dir = output / "games"
games_dir.mkdir()

results = Counter()

for game_id in range(1, 11):
    game = TicTacToe()
    pending = {"X": None, "O": None}
    moves = []
    updates = []

    def learn(symbol, reward, done, next_state=None, next_actions=None):
        previous = pending[symbol]
        if previous is None:
            return

        state, action = previous

        detail = agent.update_tracked(
            state,
            action,
            reward,
            next_state=next_state,
            next_actions=next_actions,
            done=done,
        )

        updates.append({
            "player": symbol,
            **detail,
        })
        pending[symbol] = None

    while not game.game_over:
        player = game.current_player
        state = agent.get_state(game)
        legal = game.legal_actions()

        # Complete this player's previous two-ply transition.
        learn(
            player,
            reward=0.0,
            done=False,
            next_state=state,
            next_actions=legal,
        )

        action, decision = agent.choose_action_tracked(
            state, legal, training=True
        )

        before = list(game.board)

        if not game.make_move(action):
            raise RuntimeError("Illegal self-play action")

        pending[player] = (state, action)

        moves.append({
            "player": player,
            "action": action,
            "board_before": before,
            "board_after": list(game.board),
            "decision": decision,
        })

    # Both players receive their own terminal rewards.
    for player in ("X", "O"):
        reward = (
            0.5 if game.winner is None
            else 1.0 if game.winner == player
            else -1.0
        )
        learn(player, reward=reward, done=True)

    result = game.winner or "draw"
    results[result] += 1

    record = {
        "game_id": game_id,
        "winner": result,
        "final_board": game.board,
        "moves": moves,
        "learning_updates": updates,
    }

    destination = games_dir / f"game_{game_id:04d}.json"
    with destination.open("x", encoding="utf-8") as file:
        json.dump(record, file, indent=2, default=str)

model_path = output / "model_after_10.pkl"
agent.save(str(model_path))

assert hashlib.sha256(source.read_bytes()).hexdigest() == baseline_hash

print("=== SELF-PLAY SMOKE TEST ===")
print("Games:", sum(results.values()))
print("X wins:", results["X"])
print("O wins:", results["O"])
print("Draws:", results["draw"])
print("Q-table entries:", len(agent.q_table))
print("Game files:", len(list(games_dir.glob("game_*.json"))))
print("✅ Both players trained")
print("✅ Original baseline unchanged")
print("✅ Test model saved separately")
