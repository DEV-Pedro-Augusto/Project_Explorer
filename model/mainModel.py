

class MainModel:


    def __init__(
        self,
        database: Any,
        categoria_model: Any,
        item_model: Any,
        formatModel: Any,
        usuario_model: Any,
    ):
        self.database = database
        self.categoria_model = categoria_model
        self.item_model = item_model
        self.format_model = formatModel
        self.usuario_model = usuario_model


