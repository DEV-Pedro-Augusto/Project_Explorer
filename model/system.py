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
        print("Usuário deslogado")