from agent import QLearningAgent
from game import TicTacToe


def self_play_episode(agent):
    game = TicTacToe()

    # Each player's most recent state-action pair
    pending = {"X": None, "O": None}

    while not game.game_over:
        player = game.current_player
        state = agent.get_state(game)

        # Previous action's next decision state has arrived
        if pending[player] is not None:
            old_state, old_action = pending[player]

            agent.update(
                old_state,
                old_action,
                reward=0.0,
                next_state=state,
                next_actions=game.legal_actions(),
                done=False,
            )

        action = agent.choose_action(
            state,
            game.legal_actions(),
            training=True,
        )

        game.make_move(action)
        pending[player] = (state, action)

    # Give each player its own final reward
    for player in ("X", "O"):
        if pending[player] is None:
            continue

        state, action = pending[player]

        if game.winner == player:
            reward = 1.0
        elif game.winner is None:
            reward = 0.5
        else:
            reward = -1.0

        agent.update(
            state,
            action,
            reward=reward,
            done=True,
        )

    return game.winner


if __name__ == "__main__":
    agent = QLearningAgent()

    winner = self_play_episode(agent)

    print("✅ Self-play episode completed!")
    print("Winner:", winner or "Draw")
    print("Q-table entries:", len(agent.q_table))
