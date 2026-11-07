import random
from agent import QLearningAgent
from game import TicTacToe

def evaluate(agent, games=2000, seed=42):
    random.seed(seed)
    results = {"win": 0, "loss": 0, "draw": 0}

    for episode in range(games):
        game = TicTacToe()
        ai_symbol = "X" if episode % 2 == 0 else "O"

        while not game.game_over:
            if game.current_player == ai_symbol:
                action = agent.choose_action(
                    agent.get_state(game),
                    game.legal_actions(),
                    training=False
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

models = {
    "Untrained": None,
    "After 1000 human games": "data/final_1000/q_table_live.pkl",
}

print("=== FINAL EVALUATION ===")

for name, path in models.items():
    agent = QLearningAgent(epsilon=0.0)

    if path:
        agent.load(path)

    results = evaluate(agent)

    print(f"\n{name}")
    for outcome, count in results.items():
        print(f"{outcome}: {count} ({count / 20:.1f}%)")

print("\n✅ Evaluation completed")
