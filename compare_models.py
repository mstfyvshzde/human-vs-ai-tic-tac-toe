from agent import QLearningAgent
from game import TicTacToe

v1 = QLearningAgent(epsilon=0.0)
v1.load("data/baselines/random_100k.pkl")

v2 = QLearningAgent(epsilon=0.0)
v2.load("data/q_table_v2.pkl")

results = {"v1": 0, "v2": 0, "draw": 0}

for episode in range(1000):
    game = TicTacToe()

    # Alternate first player
    v1_symbol = "X" if episode % 2 == 0 else "O"
    v2_symbol = "O" if v1_symbol == "X" else "X"

    while not game.game_over:
        agent = (
            v1 if game.current_player == v1_symbol
            else v2
        )

        state = agent.get_state(game)

        action = agent.choose_action(
            state,
            game.legal_actions(),
            training=False
        )

        game.make_move(action)

    if game.winner == v1_symbol:
        results["v1"] += 1
    elif game.winner == v2_symbol:
        results["v2"] += 1
    else:
        results["draw"] += 1

print("\nAI v1 vs AI v2 — 1,000 Games")
print("AI v1 wins:", results["v1"])
print("AI v2 wins:", results["v2"])
print("Draws:", results["draw"])
