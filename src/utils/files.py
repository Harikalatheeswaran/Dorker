"""Small filesystem helpers for reading and appending markdown data files."""

from __future__ import annotations

from pathlib import Path


def read_markdown(path: Path) -> str:
    """Return the contents of a markdown file, or a friendly placeholder."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"_File not found: `{path}`_"
    except OSError as exc:
        return f"_Could not read `{path}`: {exc}_"


def append_text(path: Path, text: str) -> None:
    """Append ``text`` to ``path``, creating the file and parents if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)
