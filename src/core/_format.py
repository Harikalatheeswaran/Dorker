"""Shared query-string formatting helpers used by every builder.

Keeping these in one place means the standard generator and the open-directory
generator render fragments (quoting, exclusions, filetypes, de-duplication,
recommendation selection) identically — no copy-paste drift.

Helpers operate on plain primitives rather than ``DorkRequest`` so they stay
decoupled and trivially testable.
"""

from __future__ import annotations

from urllib.parse import quote_plus

from src.core.models import QueryResult, QueryVariation

# Hard ceiling on variations shown for any single result, regardless of mode.
MAX_VARIATIONS_CEILING = 8


def quote(term: str) -> str:
    """Wrap a term in quotes when it contains whitespace, else return as-is."""
    term = term.strip()
    return f'"{term}"' if " " in term else term


def join(parts: list[str]) -> str:
    """Collapse query fragments into a single normalised query string."""
    return " ".join(p for p in parts if p).strip()


def keywords_fragment(keywords: list[str]) -> str:
    """Render include keywords as a quoted, space-joined fragment."""
    return " ".join(quote(k) for k in keywords if k.strip())


def excludes_fragment(keywords: list[str]) -> str:
    """Render exclude keywords as a ``-term`` fragment."""
    return " ".join(f"-{quote(k)}" for k in keywords if k.strip())


def site_fragment(site: str) -> str:
    """Render the ``site:`` operator, or an empty string when no site is set."""
    return f"site:{site.strip()}" if site.strip() else ""


def _clean_extensions(filetypes: list[str]) -> list[str]:
    """Normalise extensions: strip leading dots and whitespace, drop blanks."""
    return [t.lstrip(".").strip() for t in filetypes if t.strip()]


def filetype_or(filetypes: list[str]) -> str:
    """Render filetypes using Google's ``filetype:`` with OR for multiples."""
    types = _clean_extensions(filetypes)
    if not types:
        return ""
    if len(types) == 1:
        return f"filetype:{types[0]}"
    return "(" + " OR ".join(f"filetype:{t}" for t in types) + ")"


def filetype_group(filetypes: list[str]) -> str:
    """Render filetypes as the open-directory ``+(ext|ext)`` positive group."""
    types = _clean_extensions(filetypes)
    if not types:
        return ""
    return "+(" + "|".join(types) + ")"


def search_url(query: str, base_url: str) -> str:
    """Build a ready-to-click search URL for ``query``."""
    return f"{base_url}{quote_plus(query)}" if query else ""


def finalise(variations: list[QueryVariation], max_variations: int) -> QueryResult:
    """De-duplicate, clamp to the mode limit and select the recommendation.

    The most powerful (highest ``power``) surviving variation is recommended.
    At least two variations are kept whenever the inputs allow it.
    """
    seen: set[str] = set()
    unique: list[QueryVariation] = []
    for variation in variations:
        if variation.query and variation.query not in seen:
            seen.add(variation.query)
            unique.append(variation)

    clamped = unique[: max(2, min(max_variations, MAX_VARIATIONS_CEILING))]

    recommended_index = 0
    best_power = -1
    for index, variation in enumerate(clamped):
        if variation.power > best_power:
            best_power = variation.power
            recommended_index = index

    return QueryResult(variations=clamped, recommended_index=recommended_index)
