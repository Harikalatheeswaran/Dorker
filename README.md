

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
- **Open Directory Finder section (100% ewasion logic)** — when enabled, Dorker adds a **dedicated** `🗂️ Open Directory` section that reproduces the [ewasion/opendirectory-finder](https://github.com/ewasion/opendirectory-finder) `index.html` query builder **verbatim**: unquoted keywords, a curated `+(MOBI|EPUB|PDF|…)` filetype group, the `-inurl:(…)` noise/fake-index filters and `intitle:index.of`. Example for a Books search:
  ```text
  feynman lectures +(MOBI|CBZ|CBR|CBC|CHM|EPUB|FB2|LIT|LRF|ODT|PDF|PRC|PDB|PML|RB|RTF|TCR|DOC|DOCX) -inurl:(jsp|pl|php|html|aspx|htm|cf|shtml) intitle:index.of -inurl:(listen77|mp3raid|mp3toss|mp3drug|index_of|index-of|wallywashis|downloadmana)
  ```
  When Open Directory is enabled this exact dork becomes the **overall recommendation**. (A no-filetype "Other" variant and an optional `site:`-narrowed variant are also offered.)
- **Works in any browser / any engine** — every recommendation is shown as ready-to-click alternate links for **Google, DuckDuckGo, Bing and Startpage**. A dork is just a query string, so it is never tied to Chrome; Google honours the advanced operators (`+(...)`, `intitle:index.of`) most reliably and stays the headline.
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
and one overall recommendation. The recommendation is rendered as clickable
links for Google, DuckDuckGo, Bing and Startpage, and the raw query is copied to
your clipboard so you can paste it into any browser or search engine.

---

## ⚙️ Configuration

Open `src/config.py` to:

- Switch the default theme (`DEFAULT_THEME`) or add new ones to `THEMES`.
- Tune the variation limits per `Mode`.
- Extend `SUGGESTED_FILETYPES` or the open-directory filters
  (`OPENDIR_NOISE_EXTENSIONS`, `OPENDIR_BLOCKLIST`).

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

---

## Acknowledgements 🙌

- **[ewasion/opendirectory-finder](https://github.com/ewasion/opendirectory-finder)**
  by [**@ewasion**](https://github.com/ewasion) — the open-directory hunting
  logic in Dorker (the `intitle:"index of"` + noise/fake-index `-inurl` filtering
  approach) is directly inspired by this excellent project. 
- Huge thanks to the
  author for sharing the techniques that power the `🗂️ Open Directory` section.
  Please go star their repo! ⭐
