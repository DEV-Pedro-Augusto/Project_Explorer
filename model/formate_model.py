"""Action/interaction model."""

from __future__ import annotations

from typing import Any, Optional


class AcaoPageItem:
    """Represents an action or interaction on a page item."""

    def __init__(self, db: Optional[Any] = None):
        self.db = db

    def organiza_arquivos_car(self) -> None:
        """ Organiza os arquivos que quem vem do carrinho antes de ir para o banco online """
        
      