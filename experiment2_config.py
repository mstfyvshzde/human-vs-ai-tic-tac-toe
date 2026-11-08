from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

EXPERIMENT_ROOT = PROJECT_ROOT / "experiments" / "experiment_2"

MODELS_DIR = EXPERIMENT_ROOT / "models"
LOGS_DIR = EXPERIMENT_ROOT / "logs"
EVALUATIONS_DIR = EXPERIMENT_ROOT / "evaluations"
GAMES_DIR = EXPERIMENT_ROOT / "games"

MODEL_FILE = MODELS_DIR / "q_table_live.pkl"
SCORE_FILE = EXPERIMENT_ROOT / "scores.json"
