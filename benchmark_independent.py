"""Frozen-model benchmark against independent scripted opponents."""

import json
import random
from pathlib import Path

from game import TicTacToe
from minimax_analysis import analyze_minimax
from symmetric_agent import SymmetricQLearningAgent

ROOT = Path("experiments/experiment_2/phase_2/models")
OUTPUT = Path("experiments/experiment_2/reports/independent_benchmark.json")

MODELS = {
    "Baseline": "baseline_0300.json",
    "Final Frozen Model": "best_human_model.json",
}

GAMES_PER_ROLE = 1000
SEED = 20261108


def opponent(symbol):
    return "O" if symbol == "X" else "X"


def immediate_winning_move(board, symbol, legal):
    for action in legal:
        trial = list(board)
        trial[action] = symbol

        if any(
            all(trial[i] == symbol for i in line)
            for line in TicTacToe.WIN_LINES
        ):
            return action

    return None


def choose_opponent_move(game, strategy, rng):
    legal = game.legal_actions()

    if strategy == "Random":
        return rng.choice(legal)

    if strategy == "Tactical":
        winning = immediate_winning_move(
            game.board, game.current_player, legal
        )
        if winning is not None:
            return winning

        blocking = immediate_winning_move(
            game.board, opponent(game.current_player), legal
        )
        if blocking is not None:
            return blocking

        return rng.choice(legal)

    if strategy == "Minimax":
        analysis = analyze_minimax(
            tuple(game.board), game.current_player, legal[0]
        )
        return rng.choice(analysis["optimal_actions"])

    raise ValueError(strategy)


def play_game(agent, strategy, ai_symbol, rng):
    game = TicTacToe()

    while not game.game_over:
        legal = game.legal_actions()

        if game.current_player == ai_symbol:
            action = agent.choose_action(
                (tuple(game.board), game.current_player),
                legal,
                training=False,
            )
        else:
            action = choose_opponent_move(game, strategy, rng)

        if action not in legal or not game.make_move(action):
            raise RuntimeError("Illegal move")

    if game.winner == ai_symbol:
        return "win"

    if game.winner is None:
        return "draw"

    return "loss"


def main():
    results = {
        "seed": SEED,
        "games_per_role": GAMES_PER_ROLE,
        "training": False,
        "models": {},
    }

    for model_name, filename in MODELS.items():
        agent = SymmetricQLearningAgent(epsilon=0)

        model_data = json.loads(
            (ROOT / filename).read_text(encoding="utf-8")
        )

        for entry in model_data["entries"]:
            key = (
                (tuple(entry["board"]), entry["player"]),
                entry["action"],
            )
            if key in agent.q_table:
                raise ValueError("Duplicate model entry")
            agent.q_table[key] = float(entry["q_value"])

        results["models"][model_name] = {}

        for strategy in ("Random", "Tactical", "Minimax"):
            total = {"win": 0, "draw": 0, "loss": 0}
            by_role = {}

            for ai_symbol in ("X", "O"):
                counts = {"win": 0, "draw": 0, "loss": 0}

                for game_index in range(GAMES_PER_ROLE):
                    seed = (
                        SEED
                        + game_index
                        + (100000 if ai_symbol == "O" else 0)
                        + {
                            "Random": 0,
                            "Tactical": 200000,
                            "Minimax": 400000,
                        }[strategy]
                    )
                    rng = random.Random(seed)

                    # Agent uses Python's module-level random for Q-value ties.
                    random.seed(seed)

                    outcome = play_game(agent, strategy, ai_symbol, rng)
                    counts[outcome] += 1
                    total[outcome] += 1

                by_role[ai_symbol] = counts

            results["models"][model_name][strategy] = {
                "total": total,
                "by_role": by_role,
            }

            print(
                f"{model_name} vs {strategy}: "
                f"W={total['win']} "
                f"D={total['draw']} "
                f"L={total['loss']}"
            )
            print("  X:", by_role["X"], "O:", by_role["O"])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(results, indent=2) + "\n",
        encoding="utf-8",
    )

    print("\nResults saved:", OUTPUT)
    print("No training or model saving performed.")


if __name__ == "__main__":
    main()
