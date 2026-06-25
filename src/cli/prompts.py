"""Reusable Rich prompt helpers shared across the interface.

All user input flows through these functions so styling and validation stay
consistent and no raw ``input()``/``print()`` calls leak into the codebase.
"""

from __future__ import annotations

from rich.console import Console
from rich.prompt import Confirm, Prompt


def ask_text(console: Console, label: str, *, default: str = "") -> str:
    """Prompt for a free-text value."""
    return Prompt.ask(f"[prompt]{label}[/prompt]", default=default, console=console).strip()


def ask_choice(
    console: Console,
    label: str,
    choices: dict[str, str],
    *,
    default: str | None = None,
) -> str:
    """Render a numbered menu and return the chosen key.

    ``choices`` maps option keys to display labels. The user selects by number;
    the corresponding key is returned.
    """
    keys = list(choices.keys())
    for index, key in enumerate(keys, start=1):
        console.print(f"  [accent]{index}[/accent]. [info]{choices[key]}[/info]")

    default_num = str(keys.index(default) + 1) if default in keys else "1"
    selection = Prompt.ask(
        f"[prompt]{label}[/prompt]",
        choices=[str(i) for i in range(1, len(keys) + 1)],
        default=default_num,
        console=console,
        show_choices=False,
    )
    return keys[int(selection) - 1]


def ask_yes_no(console: Console, label: str, *, default: bool = False) -> bool:
    """Prompt for a yes/no confirmation."""
    return Confirm.ask(f"[prompt]{label}[/prompt]", default=default, console=console)


def ask_list(console: Console, label: str, *, default: str = "") -> list[str]:
    """Prompt for a comma-separated list and return cleaned, de-duplicated items."""
    raw = ask_text(console, label, default=default)
    if not raw:
        return []
    seen: set[str] = set()
    items: list[str] = []
    for chunk in raw.split(","):
        value = chunk.strip()
        if value and value.lower() not in seen:
            seen.add(value.lower())
            items.append(value)
    return items
