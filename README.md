# Human vs AI 🎮

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

## 📊 1,000 oyunluq eksperiment

Layihənin müəllifi AI-yə qarşı 1,000 XOX oyunu oynayıb.

| Nəticə | Oyun sayı |
|---|---:|
| Şahzadənin qələbələri | 472 |
| AI-nin qələbələri | 112 |
| Heç-heçə | 416 |

Final Q-table: **2,198 entries**, onlardan **611-i non-zero**.

### Evaluation

AI təlimdən əvvəl və sonra 2,000 oyunluq random-opponent qiymətləndirməsindən keçirilib.

| Göstərici | Təlimdən əvvəl | Təlimdən sonra |
|---|---:|---:|
| Win rate | 43.1% | 48.0% |
| Loss rate | 45.1% | 37.1% |
| Draw rate | 11.9% | 15.0% |

Bu nəticələr müəyyən inkişaf göstərir, lakin AI-nin optimal strategiya öyrəndiyini sübut etmir.

Oyun tarixçəsi yalnız 750–1,000-ci raundlar üçün saxlanılıb.

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
