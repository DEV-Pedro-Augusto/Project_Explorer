class SettingsView:
    def __init__(self, system):
        self.system = system
        self.ft = system.ft

    def render(self):
        return self.ft.Column([
            # Título da Página
            self.ft.Text("Configurações do Sistema", size=28, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            self.ft.Container(height=20),

            # --- SEÇÃO 1: Preferências do Aplicativo ---
            self.ft.Text("Preferências do Aplicativo", size=16, weight=self.ft.FontWeight.W_500, color=self.ft.Colors.BLUE_400),
            self.ft.Container(
                content=self.ft.Column([
                    self.ft.ListTile(
                        leading=self.ft.Icon(self.ft.Icons.DARK_MODE, color=self.ft.Colors.WHITE),
                        title=self.ft.Text("Modo Escuro", color=self.ft.Colors.WHITE),
                        subtitle=self.ft.Text("Tema visual do painel", color=self.ft.Colors.GREY_500),
                        trailing=self.ft.Switch(value=True, active_color=self.ft.Colors.BLUE_400),
                    ),
                    self.ft.ListTile(
                        leading=self.ft.Icon(self.ft.Icons.NOTIFICATIONS_ACTIVE, color=self.ft.Colors.WHITE),
                        title=self.ft.Text("Notificações de Alerta", color=self.ft.Colors.WHITE),
                        subtitle=self.ft.Text("Avisos sobre gases ou bloqueios", color=self.ft.Colors.GREY_500),
                        trailing=self.ft.Switch(value=True, active_color=self.ft.Colors.BLUE_400),
                    ),
                ]),
                bgcolor="#111827",
                border_radius=10,
                padding=10
            ),
            
            self.ft.Container(height=20),

            # --- SEÇÃO 2: Configurações do Robô/Sensores ---
            self.ft.Text("Controle de Hardware", size=16, weight=self.ft.FontWeight.W_500, color=self.ft.Colors.BLUE_400),
            self.ft.Container(
                content=self.ft.Column([
                    self.ft.ListTile(
                        leading=self.ft.Icon(self.ft.Icons.BATTERY_SAVER, color=self.ft.Colors.WHITE),
                        title=self.ft.Text("Modo Economia de Bateria", color=self.ft.Colors.WHITE),
                        subtitle=self.ft.Text("Reduz o brilho e frequência de leitura", color=self.ft.Colors.GREY_500),
                        trailing=self.ft.Switch(value=False, active_color=self.ft.Colors.BLUE_400),
                    ),
                    self.ft.ListTile(
                        leading=self.ft.Icon(self.ft.Icons.SYNC, color=self.ft.Colors.WHITE),
                        title=self.ft.Text("Taxa de Atualização", color=self.ft.Colors.WHITE),
                        subtitle=self.ft.Text("Frequência de envio de dados do sensor", color=self.ft.Colors.GREY_500),
                        trailing=self.ft.Dropdown(
                            width=150,
                            options=[
                                self.ft.dropdown.Option("Tempo Real"),
                                self.ft.dropdown.Option("A cada 1 min"),
                                self.ft.dropdown.Option("A cada 5 min"),
                            ],
                            value="Tempo Real",
                            color=self.ft.Colors.WHITE,
                            bgcolor="#1A2235",
                            border_color=self.ft.Colors.TRANSPARENT,
                            text_size=14
                        ),
                    ),
                ]),
                bgcolor="#111827",
                border_radius=10,
                padding=10
            ),
            
            self.ft.Container(height=20),

            # --- SEÇÃO 3: Conta e Segurança ---
            self.ft.Text("Conta", size=16, weight=self.ft.FontWeight.W_500, color=self.ft.Colors.BLUE_400),
            self.ft.Container(
                content=self.ft.Column([
                    self.ft.ListTile(
                        leading=self.ft.Icon(self.ft.Icons.PERSON, color=self.ft.Colors.WHITE),
                        title=self.ft.Text("Editar Perfil", color=self.ft.Colors.WHITE),
                        trailing=self.ft.Icon(self.ft.Icons.CHEVRON_RIGHT, color=self.ft.Colors.GREY_400),
                        # on_click=lambda e: print("Abrir perfil") # Exemplo de ação
                    ),
                    self.ft.ListTile(
                        leading=self.ft.Icon(self.ft.Icons.LOGOUT, color=self.ft.Colors.RED_400),
                        title=self.ft.Text("Sair da Conta", color=self.ft.Colors.RED_400),
                        on_click=lambda e: self.system.view.page.profileSelection(self.system).render()
                    ),
                ]),
                bgcolor="#111827",
                border_radius=10,
                padding=10
            ),

        ], expand=True, scroll=self.ft.ScrollMode.AUTO)