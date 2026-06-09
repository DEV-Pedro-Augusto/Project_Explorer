

class MainModel:


    def __init__(
        self,
        database,
        categoria_model,
        item_model,
        formatModel,
        usuario_model,
    ):
        self.database = database
        self.categoria_model = categoria_model
        self.item_model = item_model
        self.format_model = formatModel
        self.usuario_model = usuario_model()


