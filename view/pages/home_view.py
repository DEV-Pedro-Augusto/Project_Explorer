"""Home page."""

from __future__ import annotations

from typing import Any


class HomeView:
    """Home view page."""

    def __init__(self, parent: Any = None):
        self.parent = parent

    def render(self) -> None:
        """Render the home view."""
        # TODO: implement home view rendering
