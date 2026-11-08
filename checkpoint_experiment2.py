"""Save Experiment 2 checkpoints without touching Experiment 1."""

from pathlib import Path
import shutil

from experiment2_config import MODEL_FILE, MODELS_DIR


def save_checkpoint(game_number):
    source = Path(MODEL_FILE)

    if not source.is_file():
        raise FileNotFoundError("Experiment 2 live model not found")

    destination = MODELS_DIR / f"checkpoint_{game_number:04d}.pkl"

    if destination.exists():
        raise FileExistsError(
            f"Checkpoint already exists: {destination}"
        )

    shutil.copy2(source, destination)
    return destination
