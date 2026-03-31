"""Item model."""

from __future__ import annotations

from typing import Any, Optional


class ItemModel:
    """Represents an inventory item."""

    def __init__(self, db: Optional[Any] = None):
        self.db = db

    def list_items(self) -> list:
        """Return a list of items."""
        # TODO: implement item listing
        return []
