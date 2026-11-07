from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

EXPERIMENT_ROOT = (
    PROJECT_ROOT / "experiments" / "zero_to_hero_2"
)

LOGS_DIR = EXPERIMENT_ROOT / "logs"
MODELS_DIR = EXPERIMENT_ROOT / "models"
EVALUATIONS_DIR = EXPERIMENT_ROOT / "evaluations"

SCORE_FILE = EXPERIMENT_ROOT / "scores.json"
MODEL_FILE = MODELS_DIR / "q_table_live.pkl"

for directory in [
    LOGS_DIR,
    MODELS_DIR,
    EVALUATIONS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)
