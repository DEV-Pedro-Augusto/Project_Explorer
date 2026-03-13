"""Controller module.

This module defines the main controller used by the application.
"""

from __future__ import annotations

from typing import Any, Optional


class ControllerMain:
    """Main application controller.

    This controller is responsible for coordinating the view, models and services.
    """

    def __init__(
        self,
        view: Optional[Any] = None,
        models: Optional[Any] = None,
        services: Optional[Any] = None,
    ):
        self.view = view
        self.models = models
        self.services = services

    def construir_page(self) -> None:
        """Build the main page of the application."""
        if not self.view:
            return

        # Provide a default behavior. The view implementation should override this.
        if hasattr(self.view, "build"):
            self.view.build()
