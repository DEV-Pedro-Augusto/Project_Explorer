"""Main window implementation."""

from __future__ import annotations
from typing import Any, Optional


class MainWindow:
    """Represents the main application window."""

    def __init__(
        self,
        page: Any,
        ft: Any,
        page_animation: Any,
        button_animation: Any,
        controller: Any,
        main_view: Any,
        time_module: Any,
        threading_module: Any,
    ):
        self.page = page
        self.ft = ft
        self.page_animation = page_animation
        self.button_animation = button_animation
        self.controller = controller
        self.main_view = main_view
        self.time = time_module
        self.threading = threading_module

    def build(self) -> None:
        """Build the main window layout."""
        if hasattr(self.main_view, "build"):
            self.main_view.build()
