class System:
    
    def __init__(self, page, ft, time, mainView, models, MainTest, Controller, AppServices):
        self.page = page
        self.ft = ft 
        self.time = time 
        self.view = mainView
        self.model = models
        self.test = MainTest, 
        self.controller = Controller
        self.service = AppServices
        
        # Armazenamento de sessão do usuário logado
        self.usuario_logado = None  # Será preenchido após autenticação
        self.id_usuario_logado = None  # ID do usuário para filtros
        self.nome_usuario_logado = None  # Nome do usuário para exibição
        self.id_dispositivo_selecionado = None  # Dispositivo/carrinho atualmente selecionado
    
    def definir_usuario(self, usuario: dict):
        """Define o usuário como logado no sistema."""
        self.usuario_logado = usuario
        self.id_usuario_logado = usuario.get('id_usuarios')
        self.nome_usuario_logado = usuario.get('nomes_usuarios', 'Desconhecido')
        print(f"Usuário logado: {self.nome_usuario_logado}")
    
    def obter_usuario(self) -> dict:
        """Retorna o usuário atualmente logado."""
        return self.usuario_logado
    
    def obter_id_usuario(self) -> int:
        """Retorna o ID do usuário logado."""
        return self.id_usuario_logado
    
    def obter_nome_usuario(self) -> str:
        """Retorna o nome do usuário logado."""
        return self.nome_usuario_logado
    
    def limpar_usuario(self):
        """Limpa a sessão do usuário (logout)."""
        self.usuario_logado = None
        self.id_usuario_logado = None
        self.nome_usuario_logado = None
        self.id_dispositivo_selecionado = None
        print("Usuário deslogado")

    def definir_dispositivo(self, id_dispositivo: int):
        """Define o dispositivo/carrinho atual para filtragem nas views."""
        self.id_dispositivo_selecionado = id_dispositivo
        print(f"Dispositivo selecionado: {id_dispositivo}")

    def obter_id_dispositivo(self) -> int:
        """Retorna o ID do dispositivo/carrinho selecionado."""
        return self.id_dispositivo_selecionado

    def limpar_dispositivo(self):
        """Limpa o dispositivo selecionado."""
        self.id_dispositivo_selecionado = None