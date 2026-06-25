"""Persistence of generated queries to the markdown history log."""

from __future__ import annotations

from datetime import datetime

from src.config import HISTORY_FILE, OBJECTIVES
from src.core.models import DorkRequest, Section
from src.core.query_builder import pick_overall
from src.utils.files import append_text


def save_to_history(
    req: DorkRequest,
    sections: list[Section],
    *,
    include_all: bool = True,
) -> None:
    """Append a formatted record of this run to ``data/history.md``.

    The file is never overwritten — each run adds a new dated section. The single
    most powerful query across every section is highlighted; when ``include_all``
    is true every variation from every section is logged too.
    """
    best_section, best_variation = pick_overall(sections)
    if best_variation is None:
        return

    objective_label = OBJECTIVES.get(req.objective, OBJECTIVES["documents"]).label
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    best_section_title = best_section.title if best_section else ""

    lines: list[str] = [
        f"\n## {timestamp}\n",
        f"- **Objective:** {objective_label}"
        + ("  _(Open Directory enabled)_" if req.opendir else ""),
    ]
    if req.site:
        lines.append(f"- **Target:** `{req.site}`")
    if req.include_keywords:
        lines.append(f"- **Keywords:** {', '.join(req.include_keywords)}")
    if req.filetypes:
        lines.append(f"- **File types:** {', '.join(req.filetypes)}")

    lines.append(f"\n**⭐ Most powerful query** _(from {best_section_title})_:\n")
    lines.append("```text")
    lines.append(best_variation.query)
    lines.append("```")

    if include_all:
        for section in sections:
            if not section.result.variations:
                continue
            lines.append(f"\n### {section.title}\n")
            for index, variation in enumerate(section.result.variations, start=1):
                star = " ⭐" if index - 1 == section.result.recommended_index else ""
                lines.append(f"{index}.{star} `{variation.query}`")

    lines.append("\n---")

    append_text(HISTORY_FILE, "\n".join(lines) + "\n")
