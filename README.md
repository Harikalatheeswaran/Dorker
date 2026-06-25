

# <div align="center">🛰️ Dorker </div>


> A hacker-style, interactive CLI that forges powerful **Google dorking** queries for real-world OSINT.

Dorker walks you through a guided, cyberpunk-styled flow and generates 2–6
optimised query variations, highlights the most powerful one, and can copy it
straight to your clipboard. Built with [Rich](https://github.com/Textualize/rich).

``` 
██████   ██████  ██████  ██   ██ ███████ ██████
██   ██ ██    ██ ██   ██ ██  ██  ██      ██   ██
██   ██ ██    ██ ██████  █████   █████   ██████
██   ██ ██    ██ ██   ██ ██  ██  ██      ██   ██
██████   ██████  ██   ██ ██   ██ ███████ ██   ██
              OSINT query forge 
```


---

## ✨ Features

- **All three tiers at once** — describe your target a single time and Dorker returns three sections: `Quick Scan 🔎`, `Deep Dork 👀`, and `Dork God 🪽✨`. No need to pick a mode up front — compare them side by side.
- **2–6 scored variations per tier** — each section stars its strongest query (`⭐ BEST`), and one overall winner is highlighted across all tiers.
- **Deep-surface pivots (Dork God)** — recovers hard-to-find content via web archives, caches and paste/dump sites (great for chasing a unique identifier such as a license plate, handle or phone number that mainstream results miss).
- **Interactive query builder** — objectives, include/exclude keywords, target site, and any file types (each emitted with an explicit `filetype:` operator).
- **Open Directory Finder section** — when enabled, Dorker adds a **dedicated** `🗂️ Open Directory` section (separate from the standard tiers) that hunts `intitle:"index of"` listings with noise/fake-index filtering, inspired by [ewasion/opendirectory-finder](https://github.com/ewasion/opendirectory-finder). Keeping it standalone means your normal dorks stay accurate instead of being overwritten by index-of logic.
- **Auto clipboard copy** of the overall most powerful query.
- **Cheat sheet** rendered as Rich Markdown on demand.
- **History log** appended to `data/history.md` (never overwritten) — records every tier's variations plus the overall winner.
- **Themeable** cyberpunk UI (`minimal`, `neon`, `matrix`) defined in `config.py`.

---

## 📦 Project structure

```
Dorker/
├── src/
│   ├── main.py            # entry point
│   ├── config.py          # themes, modes, operators, file types, paths
│   ├── banner.py          # random ASCII banners
│   ├── cli/               # Rich interface + prompts
│   ├── core/              # query engine, open-dir logic, history
│   ├── utils/             # clipboard + file helpers
│   └── __init__.py
├── data/
│   ├── dorking_cheat_sheet.md
│   └── history.md
└── README.md
```

---

## 🚀 Usage

This project is managed with [`uv`](https://github.com/astral-sh/uv).

```bash
# Install dependencies
uv sync

# Run it
uv run python -m src.main
# or
uv run dorker
```

Then follow the prompts: choose an objective, enter keywords and a target, and
Dorker prints three styled sections (Quick Scan, Deep Dork, Dork God) — plus a
dedicated Open Directory section when enabled — with a starred best query in each
and one overall recommendation.

---

## ⚙️ Configuration

Open `src/config.py` to:

- Switch the default theme (`DEFAULT_THEME`) or add new ones to `THEMES`.
- Tune the variation limits per `Mode`.
- Extend `SUGGESTED_FILETYPES`, `FILETYPE_BUNDLES`, or the open-directory filters.

---

## ⚠️ Disclaimer

- Dorker is an OSINT aid for **lawful investigation, research, and information
discovery** — from security audits to helping investigators and individuals
locate publicly indexed information. 
- It only crafts search queries against
public search engines; it does not break into, exploit, or access anything
private. 
- ⚠️You are responsible for complying with all applicable laws in your
jurisdiction. Use it for good
