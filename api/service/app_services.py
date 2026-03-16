"""Application services."""

from __future__ import annotations

from typing import Any, Optional


class AppServices:
    """High-level application services.

    This class is intended to orchestrate business logic using the models.
    """

    def __init__(self, models: Optional[Any] = None):
        self.models = models

    def perform_startup_tasks(self) -> None:
        """Execute any required startup operations."""
        # TODO: implement service startup behavior
