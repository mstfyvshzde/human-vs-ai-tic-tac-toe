import pygame
from game_log import save_completed_game
import json
from pathlib import Path

from game import TicTacToe
from agent import QLearningAgent
from live_learning import LiveLearning
from messages import get_message

pygame.init()

WIDTH, HEIGHT = 520, 780
FPS = 60
ROUND_DELAY = 2000

BG = (248, 249, 251)
DARK = (30, 38, 50)
GRAY = (125, 135, 148)
WHITE = (255, 255, 255)
BORDER = (230, 233, 238)
HUMAN_COLOR = (56, 71, 95)
AI_COLOR = (213, 140, 115)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yazıq Şahzadə vs Ağıllı Mən")

clock = pygame.time.Clock()

title_font = pygame.font.SysFont("Arial", 25, bold=True)
message_font = pygame.font.SysFont("Arial", 16)
symbol_font = pygame.font.SysFont("Arial", 70, bold=True)
score_font = pygame.font.SysFont("Arial", 30, bold=True)

ai = QLearningAgent(epsilon=0.15)
DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
live_path = DATA_DIR / "q_table_live.pkl"

if live_path.exists():
    ai.load(str(live_path))
else:
    print("🧠 New AI: Untrained, starting from zero!")

learner = LiveLearning(ai, save_path=str(live_path))

game = TicTacToe()
move_history = []

SCORE_FILE = DATA_DIR / "scores.json"

def load_scores():
    if SCORE_FILE.exists():
        with SCORE_FILE.open(encoding="utf-8") as f:
            return json.load(f)

    return {"human": 0, "ai": 0, "draw": 0, "rounds": 0}

scores = load_scores()

def save_scores():
    SCORE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with SCORE_FILE.open("w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)


# First round: Human starts
starter = "human"
human_symbol = "X"
ai_symbol = "O"

round_number = scores["human"] + scores["ai"] + scores["draw"] + 1
round_end_time = None
result_recorded = False

message = (
    "Sənə jest edirəm, ilk oyuna sən başla."
)
second_message = "Amma bir də olmayacaq! 😏"

CELL = 112
GAP = 10
BOARD = CELL * 3 + GAP * 2
START_X = (WIDTH - BOARD) // 2
START_Y = 245


def start_round(first_player):
    global game
    global starter, human_symbol, ai_symbol
    global round_end_time, result_recorded
    global message, second_message

    game = TicTacToe()
    learner.pending = None
    move_history.clear()
    starter = first_player

    # The first player always uses internal X
    if starter == "human":
        human_symbol = "X"
        ai_symbol = "O"
    else:
        human_symbol = "O"
        ai_symbol = "X"

    round_end_time = None
    result_recorded = False

    message = ""
    second_message = ""


def finish_round():
    global result_recorded
    global round_end_time
    global message, second_message
    global starter

    if result_recorded:
        return

    result_recorded = True
    round_end_time = pygame.time.get_ticks()

    if game.winner == human_symbol:
        scores["human"] += 1
        starter = "human"
        message = get_message("human_win")

    elif game.winner == ai_symbol:
        scores["ai"] += 1
        starter = "ai"
        message = get_message("ai_win")

    else:
        scores["draw"] += 1
        starter = (
            "ai" if starter == "human"
            else "human"
        )
        message = get_message("draw")

    scores["rounds"] += 1
    save_scores()
    result = (
        "win" if game.winner == ai_symbol
        else "draw" if game.winner is None
        else "loss"
    )
    learner.observe(game, ai_symbol)
    learner.finish(result)
    save_completed_game(
        sum(scores[k] for k in ("human", "ai", "draw")),
        game, human_symbol, ai_symbol, move_history
    )

    scores["rounds"] += 1
    save_scores()
    second_message = ""


def draw_text(text, font, color, center):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=center)
    screen.blit(surface, rect)


running = True

while running:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if (
                event.button == 1
                and not game.game_over
                and game.current_player == human_symbol
            ):
                mx, my = event.pos

                for row in range(3):
                    for col in range(3):
                        x = START_X + col * (CELL + GAP)
                        y = START_Y + row * (CELL + GAP)

                        rect = pygame.Rect(x, y, CELL, CELL)

                        if rect.collidepoint(mx, my):
                            board_before = list(game.board)
                            moved = game.make_move(row * 3 + col)
                            if moved:
                                move_history.append({
                                    "player": "human",
                                    "position": row * 3 + col,
                                    "before": board_before,
                                    "after": list(game.board)
                                })
                                learner.observe(game, ai_symbol)
                            break

                    else:
                        continue
                    break

    # AI turn
    if (
        running
        and not game.game_over
        and game.current_player == ai_symbol
    ):
        state = ai.get_state(game)

        action = ai.choose_action(
            state,
            game.legal_actions(),
            training=True
        )

        if action is not None:
            board_before = list(game.board)
            learner.record(state, action)
            game.make_move(action)
            move_history.append({
                "player": "ai",
                "position": action,
                "before": board_before,
                "after": list(game.board)
            })
            learner.observe(game, ai_symbol)

    # Record result exactly once
    if game.game_over:
        finish_round()

    # Automatic next round
    if (
        round_end_time is not None
        and now - round_end_time >= ROUND_DELAY
    ):
        round_number = scores["human"] + scores["ai"] + scores["draw"] + 1
        start_round(starter)

    screen.fill(BG)

    # Title
    draw_text(
        "yazıq şahzadə vs ağıllı mən",
        title_font,
        DARK,
        (WIDTH // 2, 65)
    )

    # AI messages
    draw_text(
        message,
        message_font,
        GRAY,
        (WIDTH // 2, 112)
    )

    if second_message:
        draw_text(
            second_message,
            message_font,
            GRAY,
            (WIDTH // 2, 137)
        )

    # Round info
    draw_text(
        f"ROUND {round_number}",
        message_font,
        GRAY,
        (WIDTH // 2, 184)
    )

    if game.game_over:
        if game.winner == human_symbol:
            status = "ŞAHZADƏ QAZANDI!"
        elif game.winner == ai_symbol:
            status = "AI QAZANDI!"
        else:
            status = "HEÇ-HEÇƏ!"
    else:
        status = (
            "SƏNİN NÖVBƏN"
            if game.current_player == human_symbol
            else "AI-NİN NÖVBƏSİ"
        )

    draw_text(
        status,
        message_font,
        DARK,
        (WIDTH // 2, 215)
    )

    # Board
    for row in range(3):
        for col in range(3):

            x = START_X + col * (CELL + GAP)
            y = START_Y + row * (CELL + GAP)

            rect = pygame.Rect(x, y, CELL, CELL)

            pygame.draw.rect(
                screen, WHITE, rect, border_radius=18
            )

            pygame.draw.rect(
                screen, BORDER, rect,
                width=1, border_radius=18
            )

            symbol = game.board[row * 3 + col]

            if symbol is not None:
                is_human = symbol == human_symbol
                display_symbol = "S" if is_human else "A"

                color = (
                    HUMAN_COLOR if is_human
                    else AI_COLOR
                )

                draw_text(
                    display_symbol,
                    symbol_font,
                    color,
                    rect.center
                )

    # Scoreboard
    labels = [
        ("ŞAHZADƏ", scores["human"]),
        ("AĞILLI MƏN", scores["ai"]),
        ("HEÇ-HEÇƏ", scores["draw"])
    ]

    for i, (label, value) in enumerate(labels):
        x = 100 + i * 160

        draw_text(
            label,
            message_font,
            GRAY,
            (x, 650)
        )

        draw_text(
            str(value),
            score_font,
            DARK,
            (x, 690)
        )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
