import random

MESSAGES = {
    "ai_win": [
        "Gördün, ay yazıq? 😂",
        "Bir az da məşq elə, şahzadə. 😏",
        "Mən demişdim axı! 😎",
    ],
    "human_win": [
        "Bu, texniki səhv idi! 😤",
        "Bir dəqiqə... necə uddun?! 🤨",
        "Mən bilərəkdən uduzdum. 🙄",
    ],
    "draw": [
        "Bu dəfə canını qurtardın. 😏",
        "Pis oynamırsan, insan. 🤝",
        "Heç-heçə? Hələlik qəbul edirəm. 🙃",
    ],
}

last_message = None

def get_message(result):
    global last_message

    choices = [
        msg for msg in MESSAGES[result]
        if msg != last_message
    ]

    message = random.choice(choices)
    last_message = message
    return message
