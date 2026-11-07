from tactical_analysis import analyze_tactics
from minimax_analysis import analyze_minimax


class ExperimentTracker:
    def __init__(self, logger):
        self.logger = logger

    def record_ai_move(
        self,
        game_id,
        move_number,
        board_before,
        board_after,
        ai_symbol,
        action,
        decision,
    ):
        tactics = analyze_tactics(
            board_before, ai_symbol, action
        )

        optimality = analyze_minimax(
            board_before, ai_symbol, action
        )

        record = {
            "game_id": game_id,
            "move_number": move_number,
            "player": "ai",
            "ai_symbol": ai_symbol,
            "board_before": list(board_before),
            "board_after": list(board_after),
            "action": action,
            "decision": decision,
            "tactics": tactics,
            "minimax": optimality,
        }

        self.logger.log_move(**record)
        return record

    def record_human_move(
        self,
        game_id,
        move_number,
        board_before,
        board_after,
        human_symbol,
        action,
    ):
        record = {
            "game_id": game_id,
            "move_number": move_number,
            "player": "human",
            "human_symbol": human_symbol,
            "board_before": list(board_before),
            "board_after": list(board_after),
            "action": action,
        }

        self.logger.log_move(**record)
        return record
