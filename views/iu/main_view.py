"""Main view container."""

from __future__ import annotations

from typing import Any, Optional


class MainView:
    """Container for the main application pages."""

    def __init__(
        self,
        dashboard_cls: Any,
        home_cls: Any,
        inventory_cls: Any,
        login_cls: Any,
        settings_cls: Any,
    ):
        self.dashboard_cls = dashboard_cls
        self.home_cls = home_cls
        self.inventory_cls = inventory_cls
        self.login_cls = login_cls
        self.settings_cls = settings_cls

    def build(self) -> None:
        """Build the main view layout."""
        # TODO: implement view construction logic
