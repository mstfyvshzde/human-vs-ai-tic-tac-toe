import tempfile
import unittest
from pathlib import Path

from game import TicTacToe
from agent import QLearningAgent


class GameTests(unittest.TestCase):

    def test_initial_board(self):
        game = TicTacToe()
        self.assertEqual(len(game.legal_actions()), 9)

    def test_illegal_move(self):
        game = TicTacToe()
        self.assertTrue(game.make_move(0))
        self.assertFalse(game.make_move(0))
        self.assertEqual(game.current_player, "O")

    def test_winner(self):
        game = TicTacToe()

        for action in [0, 3, 1, 4, 2]:
            game.make_move(action)

        self.assertEqual(game.winner, "X")
        self.assertTrue(game.game_over)
        self.assertEqual(game.legal_actions(), [])

    def test_draw(self):
        game = TicTacToe()

        for action in [0, 1, 2, 4, 3, 5, 7, 6, 8]:
            game.make_move(action)

        self.assertTrue(game.game_over)
        self.assertIsNone(game.winner)


class AgentTests(unittest.TestCase):

    def test_legal_action(self):
        agent = QLearningAgent()
        game = TicTacToe()
        game.make_move(0)

        action = agent.choose_action(
            agent.get_state(game),
            game.legal_actions(),
            training=False
        )

        self.assertIn(action, game.legal_actions())

    def test_reward_update(self):
        agent = QLearningAgent(alpha=0.5)
        state = ("test", "X")

        agent.update(state, 2, reward=1, done=True)
        self.assertEqual(agent.q_table[(state, 2)], 0.5)

        agent.update(state, 3, reward=-1, done=True)
        self.assertEqual(agent.q_table[(state, 3)], -0.5)

    def test_save_load(self):
        agent = QLearningAgent()
        agent.q_table[("test", 1)] = 0.75

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "model.pkl"
            agent.save(str(path))

            restored = QLearningAgent()
            restored.load(str(path))

            self.assertEqual(
                restored.q_table[("test", 1)],
                0.75
            )


if __name__ == "__main__":
    unittest.main()
