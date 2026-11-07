# Quraşdırma 🇦🇿

Human vs AI — Q-learning ilə öyrənən XOX oyunu.

## Tələblər

- Python 3.10 və ya daha yeni versiya
- Git
- macOS, Windows və ya Linux

Python: https://www.python.org/downloads/
Git: https://git-scm.com/downloads

## macOS / Linux — Terminal

~~~bash
git clone https://github.com/mstfyvshzde/human-vs-ai-tic-tac-toe
cd human-vs-ai
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
~~~

## Windows — PowerShell

~~~powershell
git clone https://github.com/mstfyvshzde/human-vs-ai-tic-tac-toe
cd human-vs-ai
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
~~~

## Oyun qaydaları

- İnsan S, AI isə A kimi oynayır.
- AI boş Q-table ilə, sıfırdan başlayır.
- Oynadıqca Q-learning vasitəsilə öyrənir.
- Oyun nəticələri və öyrənilmiş model lokal saxlanılır.
- Pullü API və hazır LLM tələb olunmur.

## Məlumatların saxlanması

- data/scores.json — nəticələr
- data/q_table_live.pkl — öyrənilmiş model
- data/game_history.jsonl — gediş tarixçəsi

## Uyğunluq

macOS üzərində sınaqdan keçirilib.
Windows və Linux dəstəyi nəzərdə tutulub,
lakin bu sistemlərdə ayrıca yoxlanmalıdır.
