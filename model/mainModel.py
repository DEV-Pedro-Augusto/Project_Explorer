

class MainModel:


    def __init__(
        self,
        database: Any,
        categoria_model: Any,
        item_model: Any,
        acao_model: Any,
        usuario_model: Any,
    ):
        self.database = database
        self.categoria_model = categoria_model
        self.item_model = item_model
        self.acao_model = acao_model
        self.usuario_model = usuario_model

    def initialize(self) -> None:
        """Optional initialization steps for models."""
        # TODO: initialize models if needed
