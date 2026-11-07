import json
from pathlib import Path
from datetime import datetime


LOG_FILE = Path(__file__).resolve().parent / "data" / "game_history.jsonl"


def save_completed_game(round_id, game, human_symbol,
                        ai_symbol, moves):
    record = {
        "round": round_id,
        "timestamp": datetime.now().astimezone().isoformat(),
        "first_player": (
            "human" if human_symbol == "X" else "ai"
        ),
        "winner": (
            "human" if game.winner == human_symbol
            else "ai" if game.winner == ai_symbol
            else "draw"
        ),
        "moves": moves,
        "final_board": list(game.board),
    }

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
