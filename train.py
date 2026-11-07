import random

from agent import QLearningAgent
from game import TicTacToe


def train_episode(agent):
    game = TicTacToe()
    ai_symbol = random.choice(["X", "O"])

    while not game.game_over:
        if game.current_player != ai_symbol:
            game.make_move(random.choice(game.legal_actions()))
            continue

        state = agent.get_state(game)
        action = agent.choose_action(
            state, game.legal_actions(), training=True
        )

        game.make_move(action)

        if not game.game_over:
            opponent_action = random.choice(game.legal_actions())
            game.make_move(opponent_action)

        if game.game_over:
            if game.winner == ai_symbol:
                reward = 1.0
            elif game.winner is None:
                reward = 0.5
            else:
                reward = -1.0

            agent.update(
                state, action, reward, done=True
            )
        else:
            next_state = agent.get_state(game)
            agent.update(
                state,
                action,
                reward=0.0,
                next_state=next_state,
                next_actions=game.legal_actions(),
            )

    return game.winner, ai_symbol


def main():
    agent = QLearningAgent()
    results = {"win": 0, "loss": 0, "draw": 0}

    for episode in range(1, 1001):
        winner, ai_symbol = train_episode(agent)

        if winner == ai_symbol:
            results["win"] += 1
        elif winner is None:
            results["draw"] += 1
        else:
            results["loss"] += 1

        if episode % 200 == 0:
            print(f"Training: {episode}/1000 games")

    print("\nTraining completed!")
    print("Training outcomes:", results)
    print("Q-table entries:", len(agent.q_table))


if __name__ == "__main__":
    main()
