"""Open-directory ("index of") discovery query generator.

Inspired by ewasion/opendirectory-finder, whose core trick is to combine
``intitle:index.of`` with a positive filetype group and a negative ``-inurl``
filter that strips out rendered web pages and known fake-index link farms::

    <keywords> +(mp3|flac|...) -inurl:(jsp|php|html|...) intitle:index.of
    -inurl:(listen77|mp3raid|...)

This module reproduces that logic and layers Dorker's mode system on top so the
dedicated Open Directory section can dial its aggressiveness up or down.
"""

from __future__ import annotations

from src.config import (
    FILETYPE_BUNDLES,
    MODES,
    OPENDIR_BLOCKLIST,
    OPENDIR_NOISE_EXTENSIONS,
)
from src.core import _format as fmt
from src.core.models import DorkRequest, QueryResult, QueryVariation


def _filetype_group(req: DorkRequest) -> str:
    """Build the ``+(ext|ext)`` positive filetype group from the request.

    Falls back to a sensible bundle based on the objective when the user did not
    pick specific extensions.
    """
    group = fmt.filetype_group(req.filetypes)
    if group:
        return group
    bundle_key = {"books": "books", "documents": "documents"}.get(req.objective)
    return f"+({FILETYPE_BUNDLES[bundle_key]})" if bundle_key else ""


def _noise_filter() -> str:
    """The ``-inurl:(jsp|php|...)`` filter that removes rendered pages."""
    return "-inurl:(" + "|".join(OPENDIR_NOISE_EXTENSIONS) + ")"


def _blocklist_filter() -> str:
    """The ``-inurl:(listen77|...)`` filter that removes fake-index farms."""
    return "-inurl:(" + "|".join(OPENDIR_BLOCKLIST) + ")"


def build_opendir_queries(req: DorkRequest) -> QueryResult:
    """Generate open-directory discovery queries for ``req``."""
    mode = MODES.get(req.mode, MODES["quick"])

    keywords = fmt.keywords_fragment(req.include_keywords)
    excludes = fmt.excludes_fragment(req.exclude_keywords)
    site = fmt.site_fragment(req.site)
    filetypes = _filetype_group(req)

    variations: list[QueryVariation] = []

    # --- Variation 1: classic, human-readable index-of probe -------------- #
    variations.append(
        QueryVariation(
            query=fmt.join([keywords, 'intitle:"index of"', '"parent directory"', site, excludes]),
            rationale="Classic open-directory probe (index of + parent directory).",
            power=2 + bool(site) + bool(keywords),
        )
    )

    # --- Variation 2: filetype-focused listing ---------------------------- #
    if filetypes:
        variations.append(
            QueryVariation(
                query=fmt.join([keywords, filetypes, 'intitle:"index of"', site, excludes]),
                rationale="Open directories that actually contain your file types.",
                power=3 + bool(site) + bool(keywords),
            )
        )

    # --- Variation 3: the ewasion-style noise-filtered powerhouse --------- #
    powerhouse = fmt.join(
        [
            keywords,
            filetypes,
            _noise_filter(),
            "intitle:index.of",
            _blocklist_filter(),
            site,
            excludes,
        ]
    )
    variations.append(
        QueryVariation(
            query=powerhouse,
            rationale="Noise-filtered powerhouse — strips web pages & fake indexes.",
            power=6 + bool(site) + bool(filetypes),
        )
    )

    # Deeper modes add more surgical variants.
    if mode.key in {"deep", "god"}:
        # --- Variation 4: alternate "last modified" listing signature ----- #
        variations.append(
            QueryVariation(
                query=fmt.join(
                    [
                        keywords,
                        filetypes,
                        'intitle:"index of"',
                        '"last modified"',
                        "-inurl:(html|htm|php|asp)",
                        site,
                        excludes,
                    ]
                ),
                rationale="Targets directory listings by their 'last modified' column.",
                power=5 + bool(site) + bool(filetypes),
            )
        )

    if mode.aggressive:
        # --- Variation 5: server-banner directory listings ---------------- #
        variations.append(
            QueryVariation(
                query=fmt.join(
                    [
                        keywords,
                        filetypes,
                        'intitle:"index of /"',
                        '(intext:"apache" OR intext:"nginx")',
                        _noise_filter(),
                        site,
                        excludes,
                    ]
                ),
                rationale="Server-banner directories (Apache/Nginx auto-index pages).",
                power=5 + bool(site) + bool(filetypes),
            )
        )

    return fmt.finalise(variations, mode.max_variations)
