import flet as ft
from view.pages.main_windows import MainWindows

class MainView():
    def __init__(self, page, ft, dashboard, home_view, inventory_view, login_view, settings_view):
        self.page = page
        self.ft = ft
        self.dashboard = dashboard
        self.home_view = home_view
        self.inventory_view = inventory_view
        self.login_view = login_view
        self.settings_view = settings_view
        self.carregando = False
        self.time = __import__('time')
        self.threading = __import__('threading')

        # Referência ao container de conteúdo (setado pelo MainWindows)
        self.container_conteudo = None

        # Armazena as instâncias das views
        self._home_view_instance = None
        self._settings_view_instance = None
        self._inventory_view_instance = None

    def set_container(self, container):
        """Define o container de conteúdo vindos do MainWindows."""
        self.container_conteudo = container

    def get_home_view(self):
        if self._home_view_instance is None:
            self._home_view_instance = self.home_view(self.ft, None, None, self)
        return self._home_view_instance.build()

    def get_settings_view(self):
        if self._settings_view_instance is None:
            self._settings_view_instance = self.settings_view(self.ft, None, None, self)
        return self._settings_view_instance.build()

    def get_inventory_view(self):
        if self._inventory_view_instance is None:
            self._inventory_view_instance = self.inventory_view(self.ft, None, None, self)
        return self._inventory_view_instance.build()

    def navegar(self, index):
        if self.container_conteudo:
            self.threading.Thread(target=self._processar_navegacao, args=(index,), daemon=True).start()

    def _processar_navegacao(self, index):
        self.carregando = True
        self.threading.Thread(target=self._monitorar_tempo_carregamento, daemon=True).start()

        try:
            if index == 0:
                novo_conteudo = self.get_home_view()
            elif index == 1:
                novo_conteudo = self.dashboard(self.ft, None, None, self) if self.dashboard else self.ft.Text("Dashboard (Em construção)")
            elif index == 3:
                novo_conteudo = self.get_inventory_view()
            elif index == 4:
                novo_conteudo = self.get_settings_view()
            else:
                novo_conteudo = self.ft.Text("Em construção", size=20, color="white")
        except Exception as e:
            novo_conteudo = self.ft.Text(f"Erro: {str(e)}", color="red")

        self.carregando = False 
        
        if self.container_conteudo:
            self.container_conteudo.content = novo_conteudo
            self.container_conteudo.update()

    def _monitorar_tempo_carregamento(self):
        self.time.sleep(0.2)
        if self.carregando and self.container_conteudo:
            self.container_conteudo.content = self.ft.Text("Carregando...", size=16)
            self.container_conteudo.update()
