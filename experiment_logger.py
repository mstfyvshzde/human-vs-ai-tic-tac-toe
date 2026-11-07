import json
from datetime import datetime
from pathlib import Path


class ExperimentLogger:
    def __init__(self, root="experiments/zero_to_hero_2"):
        self.root = Path(root)
        self.logs = self.root / "logs"
        self.logs.mkdir(parents=True, exist_ok=True)

    def write(self, filename, record):
        path = self.logs / filename
        record = {
            "timestamp": datetime.now().astimezone().isoformat(),
            **record
        }

        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(
                record,
                ensure_ascii=False,
                default=str
            ) + "\n")

    def log_move(self, **record):
        self.write("moves.jsonl", record)

    def log_game(self, **record):
        self.write("games.jsonl", record)

    def log_learning(self, **record):
        self.write("learning.jsonl", record)

    def log_evaluation(self, **record):
        self.write("evaluations.jsonl", record)
