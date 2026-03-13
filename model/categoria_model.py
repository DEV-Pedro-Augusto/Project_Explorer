"""Category model."""

from __future__ import annotations

from typing import Any, Optional


class CategoriaModel:
    """Represents a category in the system."""

    def __init__(self, db: Optional[Any] = None):
        self.db = db

    def list_all(self) -> list:
        """Return all categories."""
        # TODO: implement listing logic
        return []
