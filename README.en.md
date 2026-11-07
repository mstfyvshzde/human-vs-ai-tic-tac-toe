# Human vs AI 🎮

[![Python Tests](https://github.com/mstfyvshzde/human-vs-ai-tic-tac-toe/actions/workflows/tests.yml/badge.svg)](https://github.com/mstfyvshzde/human-vs-ai-tic-tac-toe/actions/workflows/tests.yml)

### Poor Shahzada vs Smart Me

**Can an AI learn to play Tic-Tac-Toe from scratch?**

Human vs AI is an open-source Tic-Tac-Toe experiment built with Python, Pygame, and Tabular Q-learning.

The AI is not given predefined winning or blocking strategies. It knows the rules and learns the value of different actions through gameplay.

## 🚀 Installation

Python 3.10+ and Git are required.

**macOS / Linux — Terminal**

~~~bash
git clone https://github.com/mstfyvshzde/human-vs-ai-tic-tac-toe
cd human-vs-ai
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
~~~

**Windows — PowerShell**

~~~powershell
git clone https://github.com/mstfyvshzde/human-vs-ai-tic-tac-toe
cd human-vs-ai
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
~~~

For detailed instructions, see [Installation Guide](INSTALL.md).

## 🎮 How to Play

- You play as **S (Shahzada)** and the AI plays as **A (Smart Me)**.
- The human starts the first game.
- The winner starts the next round.
- After a draw, the starting player alternates.
- A new round starts automatically.
- Game results are saved locally.

## 🧠 How the AI Learns

The project uses **Tabular Q-learning**.

The AI:
- Starts with an empty Q-table.
- Uses epsilon-greedy exploration.
- Receives +1 for winning, -1 for losing, and +0.5 for a draw.
- Saves its learned values after each completed game.

No Minimax algorithm or handcrafted blocking strategy is provided.

## 📊 The 1,000-Game Experiment

The project creator played 1,000 Tic-Tac-Toe games against the AI.

| Result | Games |
|---|---:|
| Shahzada wins | 472 |
| AI wins | 112 |
| Draws | 416 |

Final Q-table: **2,198 entries**, including **611 non-zero values**.

### Evaluation

The AI was evaluated against a random opponent over 2,000 games before and after training.

| Metric | Before training | After training |
|---|---:|---:|
| Win rate | 43.1% | 48.0% |
| Loss rate | 45.1% | 37.1% |
| Draw rate | 11.9% | 15.0% |

These results suggest some improvement but do not establish that the AI learned an optimal strategy.

Detailed move history was recorded only for rounds 750–1,000.

## 💾 Local Data

The application creates a local `data/` directory containing:

- `scores.json` — scoreboard
- `q_table_live.pkl` — learned Q-values
- `game_history.jsonl` — move history

These files remain on the user's computer and are not automatically uploaded to GitHub.

## 💻 Technologies

- Python
- Pygame
- NumPy
- Tabular Q-learning

No paid API or pretrained Large Language Model is required.

Tested on macOS. Windows and Linux compatibility is intended but has not yet been independently verified.

## 👨‍💻 Authorship and AI Assistance

**Concept, experimental design, strategy, research direction, and iterative testing:** Shahzada Mustafayev.

**Code generation and implementation:** OpenAI ChatGPT, directed and tested by the project creator.

The use of ChatGPT is explicitly disclosed. Reported experimental results come from actual gameplay and evaluation.

## 🌐 Language

[Azərbaycan dilində README](README.md)

## 📄 License

This project is released under the [MIT License](LICENSE).
