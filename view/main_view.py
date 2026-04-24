import flet as ft
from view.pages.main_windows import MainWindows

class MainView():
    def __init__(self, page, ft, animador_pagina, animador_botao, controller, main_view,time,threading):
        self.page = page
        self.ft = ft
        self.animador_pagina = animador_pagina
        self.animador_botao = animador_botao
        self.controller = controller
        self.main_view = main_view
        self.carregando = False
        self.controller.view = self 
        self.time = time
        self.threading = threading



        self.main_view.homeView = self.main_view.homeView(
                    self.ft, 
                    self.animador_pagina,
                    self.animador_botao,
                    self.controller
                )
        self.main_view.configuracoesView = self.main_view.configuracoesView(
                    self.ft, 
                    self.animador_pagina,
                    self.animador_botao,
                    self.controller
                )
        self.main_view.devolucaoView = self.main_view.devolucaoView(
                    self.ft, 
                    self.animador_pagina,
                    self.animador_botao,
                    self.controller
                )
        self.main_view.emprestimoView = self.main_view.emprestimoView(
                    self.ft, 
                    self.animador_pagina,
                    self.animador_botao,
                    self.controller
                )
        self.main_view.cadastroItemView = self.main_view.cadastroItemView(
                    self.ft, 
                    self.animador_pagina,
                    self.animador_botao,
                    self.controller
                )
        self.main_view.inventarioView = self.main_view.inventarioView(
                    self.ft, 
                    self.animador_pagina,
                    self.animador_botao,
                    self.controller
                )



        self.container_conteudo = self.ft.Container(
            expand=True,
            content=self.ft.Container(), 
            padding=20
        )



    def navegar(self, index):

        self.threading.Thread(target=self._processar_navegacao, args=(index,), daemon=True).start()

    def _processar_navegacao(self, index):
        self.carregando = True


        self.threading.Thread(target=self._monitorar_tempo_carregamento, daemon=True).start()


        if index == 0:
            novo_conteudo = self._obter_conteudo_pages('HomeView',self.main_view.homeView)
        elif index == 1:
            novo_conteudo = self._obter_conteudo_pages('Dashboard',self.main_view.emprestimoView)
        elif index == 3:
              novo_conteudo =self._obter_conteudo_pages('InventoryView',self.main_view.inventarioView)
        elif index == 4:
            novo_conteudo = self._obter_conteudo_pages('SettingsView',self.main_view.configuracoesView)   
        else:
            novo_conteudo = self.ft.Text("Fim das Escolas (Em construção)")

        self.carregando = False 


        self.container_conteudo.content = novo_conteudo
        self.container_conteudo.update()

    def _monitorar_tempo_carregamento(self):

        self.time.sleep(0.2)
        if self.carregando:
            self.container_conteudo.content = self.animador_pagina(self.ft).carregamento_animacao()
            self.container_conteudo.update()



    def _obter_conteudo_pages(self,local,caminho):
        self.time.sleep(0.5) 
        if hasattr(self.main_view,local) and hasattr(caminho, 'page'):
             return caminho.page
        else:
             return self.ft.Text("Bem-vindo ao Project Explorer")






    def construir_pagina_principal(self):



        self.page.clean()

        self.page.title = "Project Explorer"
        self.page.window_width = 800
        self.page.window_height = 600
        self.page.window_resizable = True
        self.page.theme_mode = self.ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.margin = 0

        menu_lateral = self.ft.NavigationRail(
            selected_index=0,
            label_type=self.ft.NavigationRailLabelType.ALL,
            min_width=90,
            min_extended_width=220,
            group_alignment=-0.9,
            indicator_color=self.ft.Colors.BLUE_GREY_100,
            indicator_shape=self.ft.RoundedRectangleBorder(radius=12),
            leading=self.ft.Container(height=20),
            on_change=lambda e: self.navegar(e.control.selected_index),
            destinations=[
                self.ft.NavigationRailDestination(
                    icon="home",
                    label="Home",
                    selected_icon=self.ft.Icons.HOME_OUTLINED
                ),
                self.ft.NavigationRailDestination(
                    icon=self.ft.Icons.OUTBOX,
                    label="Dashboard",
                    selected_icon=self.ft.Icons.OUTBOX_OUTLINED
                ),
                self.ft.NavigationRailDestination(
                    icon="inventory",
                    label="Inventário",
                    selected_icon=self.ft.Icons.INVENTORY_2_OUTLINED
                ),
                self.ft.NavigationRailDestination(
                    icon="settings",
                    label="Configurações",
                    selected_icon=self.ft.Icons.SETTINGS_OUTLINED
                ),
            ]
        )

        layout_principal = self.ft.Column(
            expand=True,
            spacing=0,
            controls=[
                self.ft.Container(
                    content=self.ft.Text(
                        "Project Explorer",
                        size=30,
                        weight=self.ft.FontWeight.W_900,
                        selectable=True,
                    ),
                    padding=30,
                    bgcolor="grey200",
                    alignment=self.ft.alignment.center,
                    width=float('inf')
                ),
                self.ft.Row(
                    expand=True,
                    spacing=0,
                    vertical_alignment=self.ft.CrossAxisAlignment.START,
                    controls=[
                        menu_lateral,
                        self.ft.VerticalDivider(width=1, color="grey300"),
                        self.container_conteudo
                    ]
                )
            ]
        )

        self.page.add(layout_principal)
        self.navegar(0)
    
    
    
    
    
    

    
    
    
    """def __init__(self, *pages):
        super().__init__()
        self.pages = pages
def main_view(self, page: ft.Page):
        page.bgcolor = "#1A1D63"  # cor de fundo principal
        page.padding = 0
        page.spacing = 0
        # Cria uma instância de MainWindows com os argumentos necessários
        # Você precisa passar os argumentos aqui conforme definido em app_imports.py
        main_windows = MainWindows(
            page, ft, None, None, None, self, None, None
        )
        page.add(main_windows)"""
