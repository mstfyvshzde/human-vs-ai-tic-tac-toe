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
                    state,
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


agent = QLearningAgent()

print("Evaluating untrained AI...")
before = evaluate(agent)

print("Training 1,000 games...")
for _ in range(1000):
    train_episode(agent)

print("Evaluating trained AI...")
after = evaluate(agent)

print("\nRESULTS — Random Opponent")
print("Untrained:", before)
print("Trained:  ", after)

print("\nWin rates:")
print(f"Before: {before['win'] / 10:.1f}%")
print(f"After:  {after['win'] / 10:.1f}%")
