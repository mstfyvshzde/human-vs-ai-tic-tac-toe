# Human vs AI 🎮

[![Python Tests](https://github.com/mstfyvshzde/human-vs-ai-tic-tac-toe/actions/workflows/tests.yml/badge.svg)](https://github.com/mstfyvshzde/human-vs-ai-tic-tac-toe/actions/workflows/tests.yml)

### Yazıq Şahzadə vs Ağıllı Mən

**AI sıfırdan XOX oynamağı öyrənə bilərmi?**

Human vs AI — Python, Pygame və Tabular Q-learning ilə hazırlanmış açıq mənbəli Tic-Tac-Toe (XOX) eksperimentidir.

Bu layihədə AI-yə əvvəlcədən qalibiyyət və ya bloklama strategiyası verilmir. O, oyun qaydalarını bilir, lakin hansı gedişlərin faydalı olduğunu təcrübədən öyrənir.

## 🚀 Oyunu necə başladım?

Kompüterinizdə Python 3.10+ və Git quraşdırılmalıdır.

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

Ətraflı məlumat: [Quraşdırma təlimatı](INSTALL.md).

## 🎮 Necə oynanılır?

- Siz **S (Şahzadə)**, AI isə **A (Ağıllı Mən)** olaraq oynayırsınız.
- İlk oyuna insan başlayır.
- Qalib növbəti oyuna birinci başlayır.
- Heç-heçədən sonra ilk başlayan tərəf dəyişir.
- Yeni raund avtomatik açılır.
- Oyun nəticələri lokal olaraq saxlanılır.

## 🧠 AI necə öyrənir?

Layihə **Tabular Q-learning** istifadə edir.

AI:
- Q-table boş vəziyyətdə başlayır.
- Epsilon-greedy exploration vasitəsilə gedişləri sınayır.
- Qələbəyə +1, məğlubiyyətə -1, heç-heçəyə +0.5 reward alır.
- Hər tamamlanmış oyundan sonra öyrəndiklərini saxlayır.

AI-yə Minimax və ya əvvəlcədən hazırlanmış bloklama strategiyası verilmir.

## 📊 Experiment 1 — Zero-to-Hero

AI sıfır Q-table ilə başlayaraq insana qarşı 1,000 oyun oynadı.

| Nəticə | Oyun sayı |
|---|---:|
| İnsan qələbəsi | 727 |
| AI qələbəsi | 63 |
| Heç-heçə | 210 |

Sabit testdə bloklama göstəricisi 41.43%-dən 54.29%-ə yüksəldi.
Lakin AI simmetrik taxta vəziyyətləri arasında öyrəndiklərini
etibarlı şəkildə ötürə bilmədi.

**[Tam elmi hesabat](experiments/zero_to_hero_2/README.md)**

## 💾 Məlumatlar

Proqram lokal `data/` qovluğu yaradır:

- `scores.json` — oyun nəticələri
- `q_table_live.pkl` — AI-nin öyrəndiyi dəyərlər
- `game_history.jsonl` — gediş tarixçəsi

Bu fayllar şəxsi kompüterinizdə saxlanılır və GitHub-a avtomatik göndərilmir.

## 💻 Texnologiyalar

- Python
- Pygame
- NumPy
- Tabular Q-learning

Pullü API və ya hazır Large Language Model tələb olunmur.

macOS üzərində yoxlanılıb. Windows və Linux dəstəyi nəzərdə tutulub, lakin ayrıca test edilməlidir.

## 👨‍💻 Müəlliflik və AI köməyi

**İdeya, eksperiment dizaynı, strategiya, tədqiqat istiqaməti və iterativ testlər:** Şahzadə Mustafayev.

**Kodun generasiyası və implementasiyası:** OpenAI ChatGPT tərəfindən, layihə müəllifinin yönləndirməsi və testləri əsasında.

ChatGPT-nin istifadəsi açıq şəkildə qeyd olunur. Eksperiment nəticələri real oyun və evaluation məlumatlarına əsaslanır.

## 🌐 Language

[English README](README.en.md)

## 📄 License

Layihə [MIT License](LICENSE) ilə yayımlanır.

## 🎮 Oyundan görüntü

![Human vs AI Tic-Tac-Toe](assets/game-screenshot.png)
