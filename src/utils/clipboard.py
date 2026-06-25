"""Thin, dependency-tolerant wrapper around the system clipboard."""

from __future__ import annotations


def copy_to_clipboard(text: str) -> bool:
    """Copy ``text`` to the system clipboard.

    Returns ``True`` on success. Clipboard support varies wildly across
    platforms and headless environments, so any failure is swallowed and
    reported via the boolean return value rather than raising.
    """
    try:
        import pyperclip
    except ImportError:
        return False

    try:
        pyperclip.copy(text)
        return True
    except Exception:
        # pyperclip raises PyperclipException when no backend is available
        # (common on bare Linux servers). Treat as a soft failure.
        return False
