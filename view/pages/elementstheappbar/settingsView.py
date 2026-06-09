from view.pages.elementstheappbar.uploadDataView import UploadDataView


class SettingsView:
    def __init__(self, system):
        self.system = system
        self.ft = system.ft
        
        # Container principal com padding geral para respirar o layout
        self.main_content = self.ft.Container(expand=True, padding=self.ft.padding.all(24))

    def render(self):

        def voltar_para_configs():
            """Função usada pelo ProfileEditWidget para retornar ao menu de configurações."""
            self.system.view.animate.animacaoPagina.animar_widget(
                self.system, 
                self.main_content, 
                build_settings_view()
            )

        def build_settings_view():
            """Constrói o menu principal de configurações com layout moderno."""
            language = self.system.get_language()
            labels = {
                "Português": {
                    "page_title": "Configurações do Sistema",
                    "section_app": "Preferências do Aplicativo",
                    "language_title": "Idioma",
                    "language_subtitle": "Configurações de idioma do painel",
                },
                "Inglês": {
                    "page_title": "System Settings",
                    "section_app": "App Preferences",
                    "language_title": "Language",
                    "language_subtitle": "Panel language settings",
                },
                "Espanhol": {
                    "page_title": "Configuración del Sistema",
                    "section_app": "Preferencias de la Aplicación",
                    "language_title": "Idioma",
                    "language_subtitle": "Configuración de idioma del panel",
                }
            }
            text = labels.get(language, labels["Português"])

            # Função auxiliar para criar os blocos/cards de configuração padronizados
            def create_settings_card(content_control):
                return self.ft.Container(
                    content=content_control,
                    bgcolor="#161B22",  # Tom de cinza escuro azulado mais suave
                    border=self.ft.border.all(1, "#30363D"), # Borda sutil estilo GitHub dark
                    border_radius=12,
                    padding=self.ft.padding.symmetric(vertical=8, horizontal=16)
                )

            return self.ft.Column([
                # --- CABEÇALHO ---
                self.ft.Column([
                    self.ft.Text(text["page_title"], size=32, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
                    self.ft.Text("Gerencie as preferências e controle o comportamento da sua aplicação.", color=self.ft.Colors.GREY_500, size=14),
                ], spacing=4),
                
                self.ft.Container(height=10), # Espaçador inicial

                # --- SEÇÃO 1: Preferências do Aplicativo ---
                self.ft.Column([
                    self.ft.Text(text["section_app"].upper(), size=12, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.BLUE_400),
                    create_settings_card(
                        self.ft.ListTile(
                            leading=self.ft.Icon(self.ft.Icons.LANGUAGE, color=self.ft.Colors.BLUE_400),
                            title=self.ft.Text(text["language_title"], color=self.ft.Colors.WHITE, weight=self.ft.FontWeight.W_500),
                            subtitle=self.ft.Text(text["language_subtitle"], color=self.ft.Colors.GREY_500, size=13),
                            trailing=self.ft.Dropdown(
                                width=140,
                                options=[
                                    self.ft.dropdown.Option("Português"),
                                    self.ft.dropdown.Option("Inglês"),
                                    self.ft.dropdown.Option("Espanhol"),
                                ],
                                value=language,
                                color=self.ft.Colors.WHITE,
                                bgcolor="#0D1117",
                                border_color="#30363D",
                                border_radius=8,
                                text_size=14,
                                on_change=lambda e: self._change_language(e.control.value)
                            ),
                        )
                    )
                ], spacing=8),

                # --- SEÇÃO 2: Configurações do Robô/Sensores ---
                self.ft.Column([
                    self.ft.Text("INTEGRAÇÃO E DADOS", size=12, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.BLUE_400),
                    create_settings_card(
                        self.ft.ListTile(
                            leading=self.ft.Icon(self.ft.Icons.CLOUD_UPLOAD_OUTLINED, color=self.ft.Colors.GREEN_400),
                            title=self.ft.Text("Controle de Dados (Supabase)", color=self.ft.Colors.WHITE, weight=self.ft.FontWeight.W_500),
                            subtitle=self.ft.Text("Enviar dados em tempo real para o banco de dados", color=self.ft.Colors.GREY_500, size=13),
                            trailing=self.ft.ElevatedButton(
                                content=self.ft.Text("Upload", color=self.ft.Colors.WHITE),
                                bgcolor=self.ft.Colors.GREEN_400,
                                on_click=lambda e: self.system.view.animate.animacaoPagina.animar_tela(self.system, UploadDataView)
                            ),
                        )
                    )
                ], spacing=8),

                # --- SEÇÃO 3: Conta e Segurança ---
                self.ft.Column([
                    self.ft.Text("CONTA", size=12, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.BLUE_400),
                    create_settings_card(

                        
                        self.ft.Column([
                            self.ft.ListTile(
                                leading=self.ft.Icon(self.ft.Icons.PERSON_OUTLINED, color=self.ft.Colors.WHITE),
                                title=self.ft.Text("Editar Perfil", color=self.ft.Colors.WHITE, weight=self.ft.FontWeight.W_500),
                                subtitle=self.ft.Text("Altere seu nome de exibição e cores do perfil", color=self.ft.Colors.GREY_500, size=13),
                                trailing=self.ft.Icon(self.ft.Icons.CHEVRON_RIGHT, color=self.ft.Colors.GREY_600),
                                on_click=lambda e: self.system.view.animate.animacaoPagina.animar_widget(
                                    self.system, 
                                    self.main_content,
                                    self.system.view.widget.profileEdit(
                                        self.system, 
                                        "Nome Atual", 
                                        ["#0052D4", "#7F00FF"], 
                                        voltar_para_configs 
                                    ).build()
                                )
                            ),
                            self.ft.Divider(height=1, color="#30363D"), # Linha divisória sutil interna
                            self.ft.ListTile(
                                leading=self.ft.Icon(self.ft.Icons.LOGOUT, color=self.ft.Colors.RED_400),
                                title=self.ft.Text("Sair da Conta", color=self.ft.Colors.RED_400, weight=self.ft.FontWeight.W_500),
                                subtitle=self.ft.Text("Desconectar deste dispositivo", color=self.ft.Colors.GREY_500, size=13),
                                trailing=self.ft.Icon(self.ft.Icons.CHEVRON_RIGHT, color=self.ft.Colors.GREY_600),
                                on_click=lambda e: self.system.view.animate.animacaoPagina.animar_tela(
                                    self.system, 
                                    self.system.view.page.profileSelection
                                )
                            ),
                        ], spacing=0)
                    )
                ], spacing=8),

            ], expand=True, scroll=self.ft.ScrollMode.AUTO, spacing=28)

        def _change_language(value):
            self.system.set_language(value)
            self.main_content.content = build_settings_view()
            self.main_content.update()

        self._change_language = _change_language

        # Inicia a tela colocando o menu como conteúdo principal
        self.main_content.content = build_settings_view()
        return self.main_content