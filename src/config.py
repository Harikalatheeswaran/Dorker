"""Central configuration: themes, modes, operators, file types and paths.

Everything that defines *how Dorker looks and what it knows about* lives here so
the rest of the codebase stays free of magic strings and is trivial to extend.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from rich.theme import Theme

# --------------------------------------------------------------------------- #
# Filesystem paths
# --------------------------------------------------------------------------- #
# src/config.py -> project root is one level up from the package directory.
PACKAGE_DIR: Path = Path(__file__).resolve().parent
PROJECT_ROOT: Path = PACKAGE_DIR.parent
DATA_DIR: Path = PROJECT_ROOT / "data"
CHEAT_SHEET_FILE: Path = DATA_DIR / "dorking_cheat_sheet.md"
HISTORY_FILE: Path = DATA_DIR / "history.md"


# --------------------------------------------------------------------------- #
# Themes
# --------------------------------------------------------------------------- #
# Each theme maps semantic style names to Rich style strings. The application
# code only ever references the semantic names, so swapping a theme restyles the
# whole UI without touching a single view.
THEMES: dict[str, Theme] = {
    # Default: minimal cyberpunk — restrained neon on a dark canvas.
    "minimal": Theme(
        {
            "banner": "bold bright_cyan",
            "title": "bold bright_cyan",
            "subtitle": "dim cyan",
            "accent": "bright_magenta",
            "prompt": "bold bright_green",
            "info": "cyan",
            "muted": "grey50",
            "success": "bold bright_green",
            "warning": "bold yellow",
            "error": "bold red",
            "query": "bright_white",
            "recommended": "bold bright_green",
            "operator": "bright_magenta",
            "border": "cyan",
            "border.accent": "bright_magenta",
        }
    ),
    # A louder, high-contrast neon variant for those who like it bright.
    "neon": Theme(
        {
            "banner": "bold magenta",
            "title": "bold magenta",
            "subtitle": "bright_cyan",
            "accent": "bright_green",
            "prompt": "bold bright_cyan",
            "info": "bright_magenta",
            "muted": "grey58",
            "success": "bold bright_green",
            "warning": "bold bright_yellow",
            "error": "bold bright_red",
            "query": "bright_white",
            "recommended": "bold bright_green",
            "operator": "bright_green",
            "border": "magenta",
            "border.accent": "bright_green",
        }
    ),
    # Calm green-on-black "matrix" terminal feel.
    "matrix": Theme(
        {
            "banner": "bold green",
            "title": "bold green",
            "subtitle": "green",
            "accent": "bright_green",
            "prompt": "bold green",
            "info": "green",
            "muted": "grey42",
            "success": "bold bright_green",
            "warning": "bold yellow",
            "error": "bold red",
            "query": "bright_green",
            "recommended": "bold bright_green",
            "operator": "bright_green",
            "border": "green",
            "border.accent": "bright_green",
        }
    ),
}

DEFAULT_THEME: str = "minimal"


def get_theme(name: str | None = None) -> Theme:
    """Return a Rich ``Theme`` by name, falling back to the default theme."""
    return THEMES.get(name or DEFAULT_THEME, THEMES[DEFAULT_THEME])


# --------------------------------------------------------------------------- #
# Modes
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Mode:
    """A dork-generation mode controlling query depth and aggressiveness."""

    key: str
    label: str
    description: str
    max_variations: int
    aggressive: bool


MODES: dict[str, Mode] = {
    "quick": Mode(
        key="quick",
        label="Quick Scan 🔎",
        description="Minimal, fast queries — get results in seconds.",
        max_variations=3,
        aggressive=False,
    ),
    "deep": Mode(
        key="deep",
        label="Deep Dork 👀",
        description="Refined, layered queries combining multiple operators.",
        max_variations=5,
        aggressive=False,
    ),
    "god": Mode(
        key="god",
        label="Dork God 🪽✨",
        description="Maximum complexity, aggressive combos + deep/archived web pivots.",
        max_variations=8,
        aggressive=True,
    ),
}


# --------------------------------------------------------------------------- #
# Objectives
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Objective:
    """A high-level intent that biases which operators get emphasised."""

    key: str
    label: str
    description: str


OBJECTIVES: dict[str, Objective] = {
    "documents": Objective(
        "documents", "Find documents", "Locate reports, papers and files."
    ),
    "books": Objective(
        "books", "Download books", "Hunt for e-books and reading material."
    ),
    "panels": Objective(
        "panels",
        "Find login/admin panels",
        "Surface authentication and admin endpoints.",
    ),
    "directories": Objective(
        "directories",
        "Explore exposed directories",
        "Discover open 'index of' listings.",
    ),
}


# --------------------------------------------------------------------------- #
# Operators & file types
# --------------------------------------------------------------------------- #
OPERATORS: dict[str, str] = {
    "site": "Restrict results to a domain (site:example.com)",
    "filetype": "Match a specific file extension (filetype:pdf)",
    "intitle": "Word must appear in the page title (intitle:admin)",
    "inurl": "Word must appear in the URL (inurl:login)",
    "intext": "Word must appear in the page body (intext:password)",
}

# Suggested individual file types presented to the user.
SUGGESTED_FILETYPES: list[str] = [
    "pdf",
    "xml",
    "xlsx",
    "csv",
    "md",
    "mp3",
    "log",
    "json",
    "doc",
    "docx",
    "txt",
    "sql",
    "env",
    "bak",
    "conf",
    "yml",
]

# Curated filetype bundles, inspired by ewasion/opendirectory-finder. Useful for
# open-directory hunting where Google groups extensions with an OR (|) operator.
FILETYPE_BUNDLES: dict[str, str] = {
    "documents": "pdf|doc|docx|xls|xlsx|ppt|pptx|csv|txt|rtf|odt",
    "books": "MOBI|CBZ|CBR|CBC|CHM|EPUB|FB2|LIT|LRF|ODT|PDF|PRC|PDB|PML|RB|RTF|TCR|DOC|DOCX",
    "music": "mp3|wav|ac3|ogg|flac|wma|m4a|aac|mod",
    "video": "mkv|mp4|avi|mov|mpg|wmv|divx|mpeg",
    "software": "exe|iso|dmg|tar|7z|bz2|gz|rar|zip|apk",
    "images": "jpg|png|bmp|gif|tif|tiff|psd",
    "config": "env|conf|cfg|ini|yml|yaml|json|xml|log|sql|bak",
}

# Extensions that usually indicate a *rendered* web page rather than a raw,
# downloadable file. Excluding them sharpens open-directory results.
OPENDIR_NOISE_EXTENSIONS: list[str] = [
    "jsp",
    "pl",
    "php",
    "html",
    "aspx",
    "htm",
    "cf",
    "shtml",
]

# Known link-farm / fake-index hosts that pollute "index of" searches.
OPENDIR_BLOCKLIST: list[str] = [
    "listen77",
    "mp3raid",
    "mp3toss",
    "mp3drug",
    "index_of",
    "index-of",
    "wallywashis",
    "downloadmana",
]

# --------------------------------------------------------------------------- #
# Deep / low-visibility surfacing (Dork God mode)
# --------------------------------------------------------------------------- #
# Google can only return pages it has indexed, but content that is *hard to
# surface* (taken down, rewritten, mirrored, or buried) often survives in web
# archives and caches. These pivots help investigators recover it.
ARCHIVE_SITES: list[str] = [
    "web.archive.org",
    "archive.ph",
    "archive.today",
    "cachedview.nl",
    "timetravel.mementoweb.org",
]

# Public paste / text-dump / snippet hosts where leaked or unlisted content
# frequently appears before (or instead of) the mainstream web.
PASTE_SITES: list[str] = [
    "pastebin.com",
    "rentry.co",
    "ghostbin.com",
    "throwbin.io",
    "controlc.com",
    "justpaste.it",
    "telegra.ph",
]


@dataclass
class Settings:
    """Runtime settings resolved at startup (kept small and explicit)."""

    theme_name: str = DEFAULT_THEME
    clipboard_enabled: bool = True
    search_base_url: str = "https://www.google.com/search?q="
