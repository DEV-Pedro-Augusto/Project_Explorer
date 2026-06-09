class System:
    
    def __init__(self, page, ft, time,os,httpx,create_client,Client,SyncClientOptions,SUPABASE_URL,SUPABASE_KEY, mainView, models, MainTest, Controller, AppServices):
        self.page = page
        self.ft = ft 
        self.time = time 
        self.os = os
        self.httpx = httpx
        self.supabase = {"create_client":create_client,"client":Client,"SyncClientOptions":SyncClientOptions,"SUPABASE_URL":SUPABASE_URL,"SUPABASE_KEY":SUPABASE_KEY}
        self.view = mainView
        self.model = models
        self.test = MainTest
        self.controller = Controller
        self.service = AppServices

    def definir_dispositivo(self, id_dispositivo: int):
        """Define o dispositivo selecionado."""
        return self.model.usuario_model.definir_dispositivo(id_dispositivo)
    
    def obter_id_dispositivo(self) -> int:
        """Retorna o ID do dispositivo selecionado."""
        return self.model.usuario_model.obter_id_dispositivo()
    
    def obter_id_usuario(self) -> int:
        """Retorna o ID do usuário logado."""
        return self.model.usuario_model.obter_id_usuario()
    
    def definir_usuario(self, usuario: dict):
        """Define o usuário logado."""
        return self.model.usuario_model.definir_usuario(usuario)

