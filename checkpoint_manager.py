from pathlib import Path
import shutil

from experiment_config import MODEL_FILE, MODELS_DIR


def save_checkpoint(game_number):
    source = Path(MODEL_FILE)

    if not source.exists():
        raise FileNotFoundError(
            "AI model must be saved before checkpoint"
        )

    destination = MODELS_DIR / (
        f"checkpoint_{game_number:04d}.pkl"
    )

    if destination.exists():
        raise FileExistsError(
            f"Checkpoint already exists: {destination}"
        )

    shutil.copy2(source, destination)
    return destination
