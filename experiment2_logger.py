"""Experiment 2: separate, detailed record for every game."""

import json
from collections import defaultdict
from pathlib import Path

from experiment_logger import ExperimentLogger


class Experiment2Logger(ExperimentLogger):
    def __init__(self, root="experiments/experiment_2"):
        super().__init__(root=root)
        self.games_dir = self.root / "games"
        self.games_dir.mkdir(parents=True, exist_ok=True)

        self.moves = defaultdict(list)
        self.learning = defaultdict(list)

    def log_move(self, **record):
        super().log_move(**record)
        self.moves[record["game_id"]].append(record)

    def log_learning(self, **record):
        super().log_learning(**record)
        self.learning[record["game_id"]].append(record)

    def log_game(self, **record):
        game_id = record["game_id"]

        destination = self.games_dir / f"game_{game_id:04d}.json"

        if destination.exists():
            raise FileExistsError(
                f"Game file already exists: {destination}"
            )

        data = {
            "experiment": "Experiment 2",
            "game_id": game_id,
            "summary": record,
            "moves": self.moves.get(game_id, []),
            "learning_updates": self.learning.get(game_id, []),
        }

        # Serialize before creating the file.
        content = json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
            default=str,
        )

        # Prevent overwriting an existing game file.
        with destination.open("x", encoding="utf-8") as f:
            f.write(content)

        super().log_game(**record)

        self.moves.pop(game_id, None)
        self.learning.pop(game_id, None)

        print(f"✅ Game {game_id} saved")
