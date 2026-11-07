import csv
import random

from agent import QLearningAgent
from game import TicTacToe
from train import train_episode


def evaluate(agent, games=1000):
    results = {"win": 0, "loss": 0, "draw": 0}

    for episode in range(games):
        game = TicTacToe()
        ai_symbol = "X" if episode % 2 == 0 else "O"

        while not game.game_over:
            if game.current_player == ai_symbol:
                state = agent.get_state(game)
                action = agent.choose_action(
                    state, game.legal_actions(), training=False
                )
            else:
                action = random.choice(game.legal_actions())

            game.make_move(action)

        if game.winner == ai_symbol:
            results["win"] += 1
        elif game.winner is None:
            results["draw"] += 1
        else:
            results["loss"] += 1

    return results


random.seed(42)
agent = QLearningAgent()

milestones = [0, 1000, 10000, 50000, 100000]
completed = 0
records = []

for target in milestones:
    for _ in range(target - completed):
        train_episode(agent)

    completed = target

    results = evaluate(agent)
    win_rate = results["win"] / 10

    records.append({
        "training_games": target,
        "opponent": "random",
        "evaluation_games": 1000,
        "wins": results["win"],
        "losses": results["loss"],
        "draws": results["draw"],
        "win_rate": win_rate,
    })

    print(
        f"{target:>6} games | "
        f"Win: {win_rate:.1f}% | "
        f"Loss: {results['loss'] / 10:.1f}% | "
        f"Draw: {results['draw'] / 10:.1f}%"
    )

with open("training_results.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

print("\n✅ Results saved: training_results.csv")
