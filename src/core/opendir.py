"""Open-directory ("index of") discovery query generator.

This module reproduces the query logic from ewasion/opendirectory-finder's
``index.html`` **verbatim**. ewasion's builder is::

    // with a filetype group:
    <query> +(<group>) -inurl:(jsp|pl|php|html|aspx|htm|cf|shtml)
            intitle:index.of
            -inurl:(listen77|mp3raid|mp3toss|mp3drug|index_of|index-of|wallywashis|downloadmana)

    // "Other" (no filetype): identical, minus the +(...) group

Details that make ewasion's dorks reliably return results:

* the query keywords are **unquoted** (open-directory titles vary in spacing),
* it uses ``intitle:index.of`` (the ``.`` matches any char) — not ``filetype:``,
* the filetype set is a curated ``+(ext|ext|...)`` group, not a single type,
* no ``site:`` is applied to the core dork.

Credit: https://github.com/ewasion/opendirectory-finder by @ewasion.
"""

from __future__ import annotations

from src.config import (
    EWASION_FILETYPE_GROUPS,
    OPENDIR_BLOCKLIST,
    OPENDIR_NOISE_EXTENSIONS,
)
from src.core import _format as fmt
from src.core.models import DorkRequest, QueryResult, QueryVariation

# Map Dorker objectives to ewasion's predefined filetype groups. ewasion has no
# dedicated "documents" group, but its Books group already contains every common
# document type (PDF/DOC/DOCX/ODT/RTF...), so it is the faithful fallback.
_OBJECTIVE_TO_EWASION_GROUP: dict[str, str] = {
    "books": "books",
    "documents": "books",
}


def _filetype_group(req: DorkRequest) -> str:
    """Return ewasion's ``+(ext|ext)`` group, or '' for the 'Other' (no-type) path.

    The user's own extensions win when provided; otherwise fall back to the
    ewasion group mapped from the objective.
    """
    if req.filetypes:
        exts = "|".join(t.lstrip(".").strip() for t in req.filetypes if t.strip())
        return f"+({exts})" if exts else ""
    key = _OBJECTIVE_TO_EWASION_GROUP.get(req.objective)
    return f"+({EWASION_FILETYPE_GROUPS[key]})" if key else ""


def _noise_filter() -> str:
    """ewasion's ``-inurl:(jsp|pl|php|...)`` filter that removes rendered pages."""
    return "-inurl:(" + "|".join(OPENDIR_NOISE_EXTENSIONS) + ")"


def _blocklist_filter() -> str:
    """ewasion's ``-inurl:(listen77|...)`` filter that removes fake-index farms."""
    return "-inurl:(" + "|".join(OPENDIR_BLOCKLIST) + ")"


def _ewasion_query(keywords: str, group: str, extra: str = "") -> str:
    """Assemble ewasion's exact query template (optionally narrowed by ``extra``)."""
    return fmt.join(
        [
            keywords,
            group,
            _noise_filter(),
            "intitle:index.of",
            _blocklist_filter(),
            extra,
        ]
    )


def build_opendir_queries(req: DorkRequest) -> QueryResult:
    """Generate open-directory queries that mirror ewasion's logic exactly."""
    keywords = fmt.plain_keywords_fragment(req.include_keywords)
    group = _filetype_group(req)

    variations: list[QueryVariation] = []

    # --- Variation 1: the exact ewasion dork (headline) ------------------- #
    variations.append(
        QueryVariation(
            query=_ewasion_query(keywords, group),
            rationale="ewasion/opendirectory-finder exact logic — index.of + noise & fake-index filters.",
            power=8,
        )
    )

    # --- Variation 2: ewasion 'Other' path (no filetype group) ------------ #
    # Broader net — same logic without restricting to specific extensions.
    if group:
        variations.append(
            QueryVariation(
                query=_ewasion_query(keywords, ""),
                rationale="ewasion 'Other' variant — same logic, any file type.",
                power=6,
            )
        )

    # --- Variation 3: ewasion dork narrowed to the user's site/exclusions - #
    # ewasion has no site filter, so this only appears when the user supplied
    # one. Pure ewasion stays the headline above.
    extra = fmt.join([fmt.site_fragment(req.site), fmt.excludes_fragment(req.exclude_keywords)])
    if extra:
        variations.append(
            QueryVariation(
                query=_ewasion_query(keywords, group, extra),
                rationale="ewasion logic narrowed to your site / exclusions.",
                power=7,
            )
        )

    return fmt.finalise(variations, fmt.MAX_VARIATIONS_CEILING)

