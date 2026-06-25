"""The interactive Dorker application — pure Rich, zero raw prints."""

from __future__ import annotations

from rich.align import Align
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from src.banner import get_random_banner
from src.cli.prompts import ask_choice, ask_list, ask_text, ask_yes_no
from src.config import (
    CHEAT_SHEET_FILE,
    OBJECTIVES,
    OPERATORS,
    SUGGESTED_FILETYPES,
    Settings,
    get_theme,
)
from src.core import build_sections, pick_overall, save_to_history
from src.core.models import DorkRequest, QueryResult, QueryVariation, Section
from src.utils import copy_to_clipboard, read_markdown


class DorkerApp:
    """Top-level controller wiring prompts, the query engine and rendering."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        self.console = Console(theme=get_theme(self.settings.theme_name))

    # ------------------------------------------------------------------ #
    # Public entry point
    # ------------------------------------------------------------------ #
    def run(self) -> None:
        """Drive a full interactive session from banner to history."""
        self._render_banner()
        self._render_intro()

        request = self._collect_request()
        sections = build_sections(request)
        self._render_sections(sections)

        best_section, best_variation = pick_overall(sections)
        self._render_overall(best_section, best_variation)
        self._offer_clipboard(best_variation)
        self._offer_cheat_sheet()
        self._offer_history(request, sections)

        self.console.print(
            Panel(
                Align.center(Text("Happy Hunting 🎃", style="success")),
                border_style="border.accent",
            )
        )

    # ------------------------------------------------------------------ #
    # Rendering helpers
    # ------------------------------------------------------------------ #
    def _render_banner(self) -> None:
        banner = Text(get_random_banner(), style="banner")
        self.console.print(
            Panel(
                Align.center(banner),
                border_style="border",
                subtitle="[subtitle]OSINT dork forge[/subtitle]",
                padding=(1, 4),
            )
        )

    def _render_intro(self) -> None:
        body = Text.assemble(
            ("Craft surgical Google dorks through a guided flow.\n", "info"),
            (
                "Describe your target once — Dorker returns all three tiers "
                "(Quick Scan, Deep Dork, Dork God), plus a dedicated Open "
                "Directory section when enabled.",
                "muted",
            ),
        )
        self.console.print(Panel(body, title="[title]Welcome[/title]", border_style="border"))

    def _render_sections(self, sections: list[Section]) -> None:
        """Render each section: a centred header, then its variation panels."""
        for section in sections:
            count = len(section.result.variations)
            self.console.print(
                Panel(
                    Align.center(Text(section.title, style="title")),
                    subtitle=f"[subtitle]{section.description}  ·  {count} queries[/subtitle]",
                    border_style="border.accent",
                    padding=(0, 2),
                )
            )
            self._render_variations(section.result)

    def _render_variations(self, result: QueryResult) -> None:
        """Render the variation panels for a single section's result."""
        if not result.variations:
            self.console.print(
                Panel(
                    Text("No queries for this section with the given inputs.", style="muted"),
                    border_style="border",
                )
            )
            return

        for index, variation in enumerate(result.variations):
            is_recommended = index == result.recommended_index
            label_style = "recommended" if is_recommended else "query"
            star = " ⭐ BEST" if is_recommended else ""
            body = Group(
                Text(variation.query, style=label_style),
                Text(""),
                Text(variation.rationale, style="muted"),
            )
            self.console.print(
                Panel(
                    body,
                    title=f"[accent]Variation {index + 1}[/accent]{star}",
                    border_style="border.accent" if is_recommended else "border",
                    padding=(1, 2),
                )
            )

    def _render_overall(
        self, section: Section | None, variation: QueryVariation | None
    ) -> None:
        """Render the single strongest query found across every section."""
        if variation is None:
            return
        from urllib.parse import quote_plus

        url = f"{self.settings.search_base_url}{quote_plus(variation.query)}"
        source = section.title if section else ""
        self.console.print(
            Panel(
                Group(
                    Text(f"Most powerful query (from {source}):", style="success"),
                    Text(variation.query, style="recommended"),
                    Text(""),
                    Text(url, style="muted"),
                ),
                title="[success]★ Overall Recommendation[/success]",
                border_style="border.accent",
                padding=(1, 2),
            )
        )

    # ------------------------------------------------------------------ #
    # Input collection
    # ------------------------------------------------------------------ #
    def _collect_request(self) -> DorkRequest:
        request = DorkRequest()

        # Open directory mode ---------------------------------------------
        request.opendir = ask_yes_no(
            self.console,
            "Enable Open Directory Finder mode? (hunt 'index of' listings)",
            default=False,
        )

        # Objective --------------------------------------------------------
        self.console.print(Panel(Text("What is your objective?", style="title"), border_style="border"))
        request.objective = ask_choice(
            self.console,
            "Objective",
            {key: f"{obj.label} — {obj.description}" for key, obj in OBJECTIVES.items()},
            default="documents",
        )

        # Keywords ---------------------------------------------------------
        self.console.print(
            Panel(
                Text("Keywords — comma separated. Leave blank to skip.", style="muted"),
                title="[title]Keywords[/title]",
                border_style="border",
            )
        )
        request.include_keywords = ask_list(self.console, "Include keywords")
        request.exclude_keywords = ask_list(self.console, "Exclude keywords")

        # Target site ------------------------------------------------------
        request.site = ask_text(self.console, "Target domain/site (e.g. example.com, blank = any)")

        # File types -------------------------------------------------------
        self._render_filetype_hint()
        request.filetypes = ask_list(self.console, "File types (comma separated, blank = none)")

        return request

    def _render_filetype_hint(self) -> None:
        suggestions = ", ".join(f".{ext}" for ext in SUGGESTED_FILETYPES)
        operators = "\n".join(
            f"[operator]{name}:[/operator] [muted]{desc}[/muted]"
            for name, desc in OPERATORS.items()
        )
        body = Group(
            Text("Suggested file types:", style="info"),
            Text(suggestions, style="muted"),
            Text(""),
            Text("Operators in play:", style="info"),
            Text.from_markup(operators),
            Text(""),
            Text("You may enter ANY extension — not just the suggestions.", style="accent"),
        )
        self.console.print(Panel(body, title="[title]File types & operators[/title]", border_style="border"))

    # ------------------------------------------------------------------ #
    # Post-generation actions
    # ------------------------------------------------------------------ #
    def _offer_clipboard(self, variation: QueryVariation | None) -> None:
        if variation is None or not self.settings.clipboard_enabled:
            return
        if ask_yes_no(self.console, "Copy the most powerful query to clipboard?", default=True):
            if copy_to_clipboard(variation.query):
                self.console.print(
                    Panel(Text("Copied to clipboard.", style="success"), border_style="border.accent")
                )
            else:
                self.console.print(
                    Panel(
                        Text("Clipboard unavailable on this system — copy manually above.", style="warning"),
                        border_style="warning",
                    )
                )

    def _offer_cheat_sheet(self) -> None:
        if not ask_yes_no(self.console, "Do you want to view the dorking cheat sheet?", default=False):
            return
        markdown = Markdown(read_markdown(CHEAT_SHEET_FILE))
        self.console.print(
            Panel(markdown, title="[title]Dorking Cheat Sheet[/title]", border_style="border", padding=(1, 2))
        )

    def _offer_history(self, request: DorkRequest, sections: list[Section]) -> None:
        _, best_variation = pick_overall(sections)
        if best_variation is None:
            return
        if not ask_yes_no(self.console, "Save these results to history?", default=True):
            return
        include_all = ask_yes_no(self.console, "Include all variations (every section)?", default=True)
        save_to_history(request, sections, include_all=include_all)
        self.console.print(
            Panel(Text("Saved to data/history.md", style="success"), border_style="border.accent")
        )
