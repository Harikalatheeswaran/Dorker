"""Core domain logic: query models, builders and history persistence."""

from src.core.models import DorkRequest, QueryResult, QueryVariation, Section
from src.core.query_builder import build_queries, build_sections, pick_overall
from src.core.opendir import build_opendir_queries
from src.core.history import save_to_history

__all__ = [
    "DorkRequest",
    "QueryResult",
    "QueryVariation",
    "Section",
    "build_queries",
    "build_sections",
    "pick_overall",
    "build_opendir_queries",
    "save_to_history",
]
