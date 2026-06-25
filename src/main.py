"""Dorker entry point.

Run with ``python -m src.main`` or the installed ``dorker`` console script.
"""

from __future__ import annotations

import sys

from src.cli import DorkerApp
from src.config import Settings


def _force_utf8() -> None:
    """Ensure stdout/stderr use UTF-8 so emojis/box-drawing survive redirection.

    On Windows the console defaults to a legacy code page (e.g. cp1252) when
    output is piped or redirected, which would crash on Dorker's banners.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass


def main() -> None:
    """Launch the interactive Dorker session."""
    _force_utf8()
    app = DorkerApp(Settings())
    try:
        app.run()
    except (KeyboardInterrupt, EOFError):
        app.console.print("\n[warning]Aborted. Stay sharp.[/warning]")


if __name__ == "__main__":
    main()
