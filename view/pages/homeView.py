class HomeView():
    def __init__(self, system):
        self.system = system
        self.page = system.page
        self.ft = system.ft
        
        self.carregando = False
        self.time = __import__('time')
        self.threading = __import__('threading')

        # Cache das instâncias (Lazy Load)
        self._dashboard_instance = None
        self._settings_view_instance = None
        self._notifications_instance = None
        self._speed_instance = None
        self._calendar_instance = None
        self._events_instance = None

        self.container_conteudo = self.ft.Container(
            expand=True,
            content=self.ft.Container(), 
            padding=20
        )

    # --- GETTERS DAS VIEWS ---
    def get_dashboard_view(self):
        if self._dashboard_instance is None:
            self._dashboard_instance = self.system.view.page.elementsTheAppbar.dashboard(self.system, "Robô de Teste")
        return self._dashboard_instance

    def get_settings_view(self):
        if self._settings_view_instance is None:
            self._settings_view_instance = self.system.view.page.elementsTheAppbar.settings(self.system)
        return self._settings_view_instance

    def get_notifications_view(self):
        if self._notifications_instance is None:
            self._notifications_instance = self.system.view.page.elementsTheAppbar.notifications(self.system)
        return self._notifications_instance

    def get_speed_view(self):
        if self._speed_instance is None:
            self._speed_instance = self.system.view.page.elementsTheAppbar.speed(self.system)
        return self._speed_instance

    def get_calendar_view(self):
        if self._calendar_instance is None:
            self._calendar_instance = self.system.view.page.elementsTheAppbar.calendar(self.system)
        return self._calendar_instance

    def get_events_view(self):
        if self._events_instance is None:
            self._events_instance = self.system.view.page.elementsTheAppbar.events(self.system)
        return self._events_instance

    # --- LÓGICA DE NAVEGAÇÃO ---
    def navegar(self, index):
        self.threading.Thread(target=self._processar_navegacao, args=(index,), daemon=True).start()

    def _processar_navegacao(self, index):
        self.carregando = True
        self.threading.Thread(target=self._monitorar_tempo_carregamento, daemon=True).start()

        if index == 0:
            novo_conteudo = self._obter_conteudo_pages('Dashboard', self.get_dashboard_view())
        elif index == 1:
            novo_conteudo = self._obter_conteudo_pages('Notificações', self.get_notifications_view())
        elif index == 2:
            novo_conteudo = self._obter_conteudo_pages('Velocidade', self.get_speed_view())
        elif index == 3:
            novo_conteudo = self._obter_conteudo_pages('Calendário', self.get_calendar_view())
        elif index == 4:
            novo_conteudo = self._obter_conteudo_pages('Eventos', self.get_events_view())
        elif index == 5:
            novo_conteudo = self._obter_conteudo_pages('Configurações', self.get_settings_view())
        else:
            novo_conteudo = self.ft.Text("Erro: Tela não encontrada", color=self.ft.Colors.WHITE)

        self.carregando = False 
        self.container_conteudo.content = novo_conteudo
        self.container_conteudo.update()

    def _monitorar_tempo_carregamento(self):
        self.time.sleep(0.2)
        if self.carregando:
            self.container_conteudo.content = self.ft.Text("Carregando...", color=self.ft.Colors.WHITE)
            self.container_conteudo.update()

    def _obter_conteudo_pages(self, nome_view, view_instance):
        if hasattr(view_instance, 'render'):
            return view_instance.render()
        return self.ft.Text(f"{nome_view} (Em construção)", color=self.ft.Colors.WHITE)

    # --- FUNÇÃO DO BOTÃO SAIR ---
    def voltar_para_profile(self, e):
        """Limpa a tela e renderiza a ProfileSelectionView"""
        # Puxa a classe profileSelection do seu MainWindow
        profile_class = self.system.view.page.profileSelection
        profile_instance = profile_class(self.system)
        
        # Renderiza a tela de perfil
        if hasattr(profile_instance, 'render'):
            profile_instance.render()

    # --- CONSTRUÇÃO DA PÁGINA PRINCIPAL ---
    def render(self):
        self.page.clean()
        self.page.padding = 0
        self.page.margin = 0
        self.page.bgcolor = "#060A14"

        menu_lateral = self.ft.NavigationRail(
            selected_index=0,
            label_type=self.ft.NavigationRailLabelType.NONE, 
            bgcolor="#060A14",
            indicator_color="#1A2235",
            min_width=70,
            group_alignment=-0.9,
            on_change=lambda e: self.navegar(e.control.selected_index),
            destinations=[
                self.ft.NavigationRailDestination(icon=self.ft.Icons.HOME_OUTLINED, selected_icon=self.ft.Icons.HOME),
                self.ft.NavigationRailDestination(icon=self.ft.Icons.NOTIFICATIONS_OUTLINED, selected_icon=self.ft.Icons.NOTIFICATIONS),
                self.ft.NavigationRailDestination(icon=self.ft.Icons.SPEED_OUTLINED, selected_icon=self.ft.Icons.SPEED),
                self.ft.NavigationRailDestination(icon=self.ft.Icons.CALENDAR_TODAY_OUTLINED, selected_icon=self.ft.Icons.CALENDAR_TODAY),
                self.ft.NavigationRailDestination(icon=self.ft.Icons.EMOJI_EVENTS_OUTLINED, selected_icon=self.ft.Icons.EMOJI_EVENTS),
                self.ft.NavigationRailDestination(icon=self.ft.Icons.SETTINGS_OUTLINED, selected_icon=self.ft.Icons.SETTINGS),
            ]
        )

        layout_principal = self.ft.Column(
            expand=True,
            spacing=0,
            controls=[
                # --- CABEÇALHO COM TÍTULO E BOTÃO DE SAIR ---
                self.ft.Container(
                    content=self.ft.Row(
                        controls=[
                            self.ft.Text(
                                "Controllers the Car Sensor",
                                size=24,
                                weight=self.ft.FontWeight.W_900,
                                color=self.ft.Colors.WHITE,
                                selectable=True,
                            ),
                            # Botão de Sair no canto direito
                            self.ft.IconButton(
                                icon=self.ft.Icons.LOGOUT,
                                icon_color=self.ft.Colors.RED_400,
                                icon_size=28,
                                tooltip="Sair para Seleção de Perfil",
                                on_click=self.voltar_para_profile
                            )
                        ],
                        alignment=self.ft.MainAxisAlignment.SPACE_BETWEEN, # Separa título (esquerda) e botão (direita)
                        vertical_alignment=self.ft.CrossAxisAlignment.CENTER
                    ),
                    padding=20,
                    bgcolor="#060A14",
                    width=float('inf')
                ),
                # --- CORPO PRINCIPAL (Menu Lateral + Conteúdo) ---
                self.ft.Row(
                    expand=True,
                    spacing=0,
                    vertical_alignment=self.ft.CrossAxisAlignment.START,
                    controls=[
                        menu_lateral,
                        self.ft.VerticalDivider(width=1, color="#1A2235"),
                        self.container_conteudo
                    ]
                )
            ]
        )

        self.page.add(layout_principal)
        self.navegar(0)