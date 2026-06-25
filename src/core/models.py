"""Immutable data models passed between the CLI and the query engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import quote_plus

@dataclass
class DorkRequest:
    """A fully-specified request describing what the user wants to find.

    The CLI layer is responsible for populating this; the query builders consume
    it. Keeping everything in one object means adding a new input later only
    touches this class and the builders — never the call sites in between.
    """

    mode: str = "quick"
    objective: str = "documents"
    include_keywords: list[str] = field(default_factory=list)
    exclude_keywords: list[str] = field(default_factory=list)
    site: str = ""
    filetypes: list[str] = field(default_factory=list)
    # Open-directory mode toggles a different generator entirely.
    opendir: bool = False


@dataclass
class QueryVariation:
    """A single generated dork query plus a human-readable rationale."""

    query: str
    rationale: str
    # Higher = more powerful/specific. Used to pick the recommended query.
    power: int = 0


@dataclass
class QueryResult:
    """The full output of a generation run."""

    variations: list[QueryVariation] = field(default_factory=list)
    recommended_index: int = 0

    @property
    def recommended(self) -> QueryVariation | None:
        """Return the recommended variation, if any were generated."""
        if not self.variations:
            return None
        return self.variations[self.recommended_index]

    def search_url(self, base_url: str) -> str:
        """Build a ready-to-click search URL for the recommended query."""
        recommended = self.recommended
        if recommended is None:
            return ""
        return f"{base_url}{quote_plus(recommended.query)}"


@dataclass
class Section:
    """A titled block of results shown as its own panelled section in the UI.

    Sections let us present the standard Quick/Deep/God tiers *and* a dedicated
    Open Directory block side by side without conflating their queries.
    """

    key: str
    title: str
    description: str
    result: QueryResult
