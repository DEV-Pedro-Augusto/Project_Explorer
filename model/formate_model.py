"""Action/interaction model."""

from __future__ import annotations

from typing import Any, Optional


class DadosBruto:
    """Represents an action or interaction on a page item."""

    def __init__(self, db: Optional[Any] = None):
        self.db = db

    def organiza_arquivos_car(self) -> json:
        
        """ Organiza os arquivos que quem vem do carrinho antes de ir para o banco online """

        
class DadosFormatados:
    def __init__(self, db):
        self.db = {}

    def organiza_uso(self, db) -> dict:
        "Organiza os dados para uso no sistema Desktop"
        for dados in db:
            for sensor,status in dados.sensores:
                list
                pass
        






