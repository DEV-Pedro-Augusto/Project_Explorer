import flet as ft

class SettingsView:
    def __init__(self, system):
        self.system = system
        self.ft = system.ft
        
        # Guardas de caminhos dos arquivos selecionados
        self.caminho_gases = None
        self.caminho_movimento = None
        
        # Elementos de texto para dar feedback visual na tela
        self.txt_gases = self.ft.Text("Nenhum arquivo selecionado", color=self.ft.Colors.GREY_500, size=12)
        self.txt_movimento = self.ft.Text("Nenhum arquivo selecionado", color=self.ft.Colors.GREY_500, size=12)
        self.txt_status = self.ft.Text("", size=14, weight=self.ft.FontWeight.W_500)
        
        # Instancia os componentes FilePicker do Flet
        self.picker_gases = self.ft.FilePicker(on_result=self._resultado_gases)
        self.picker_movimento = self.ft.FilePicker(on_result=self._resultado_movimento)
        
        # Adiciona os pickers na página overlay do sistema para que possam ser abertos
        self.system.page.overlay.append(self.picker_gases)
        self.system.page.overlay.append(self.picker_movimento)

    def _resultado_gases(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.caminho_gases = e.files[0].path
            self.txt_gases.value = f"Selecionado: {e.files[0].name}"
            self.txt_gases.color = self.ft.Colors.GREEN_400
            self.system.page.update()

    def _resultado_movimento(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.caminho_movimento = e.files[0].path
            self.txt_movimento.value = f"Selecionado: {e.files[0].name}"
            self.txt_movimento.color = self.ft.Colors.GREEN_400
            self.system.page.update()

    def _disparar_importacao(self, e):
        if not self.caminho_gases or not self.caminho_movimento:
            self.txt_status.value = "⚠️ Por favor, selecione ambos os arquivos CSV!"
            self.txt_status.color = self.ft.Colors.ORANGE_400
            self.system.page.update()
            return
        
        # Recupera as referências dinâmicas do usuário atual e do dispositivo/carrinho ativo
        id_usuario = getattr(self.system, "usuario_logado_id", 1) 
        id_dispositivo = getattr(self.system, "dispositivo_ativo_id", 1) 
        
        self.txt_status.value = "⏳ Processando pipeline e enviando lotes..."
        self.txt_status.color = self.ft.Colors.BLUE_400
        self.system.page.update()
        
        # Executa o processo completo de ponta a ponta chamando o Database do seu sistema
        sucesso = self.system.db.importar_telemetria_supabase(
            path_gases=self.caminho_gases,
            path_movimento=self.caminho_movimento,
            id_usuario=id_usuario,
            id_dispositivo=id_dispositivo,
            descricao="Importação manual de telemetria via Painel de Configurações"
        )
        
        if sucesso:
            self.txt_status.value = "✅ Telemetria importada e sincronizada com sucesso!"
            self.txt_status.color = self.ft.Colors.GREEN_400
            # Limpa a seleção após o sucesso
            self.caminho_gases = None
            self.caminho_movimento = None
            self.txt_gases.value = "Nenhum arquivo selecionado"
            self.txt_gases.color = self.ft.Colors.GREY_500
            self.txt_movimento.value = "Nenhum arquivo selecionado"
            self.txt_movimento.color = self.ft.Colors.GREY_500
        else:
            self.txt_status.value = "❌ Erro ao processar ou enviar dados. Verifique o console."
            self.txt_status.color = self.ft.Colors.RED_400
            
        self.system.page.update()

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

            # --- SEÇÃO: Pipeline de Telemetria ---
            self.ft.Text("Importação de Dados (Pipeline)", size=16, weight=self.ft.FontWeight.W_500, color=self.ft.Colors.BLUE_400),
            self.ft.Container(
                content=self.ft.Column([
                    # Seletor do arquivo de gases
                    self.ft.ListTile(
                        leading=self.ft.Icon(self.ft.Icons.GAS_METER, color=self.ft.Colors.WHITE),
                        title=self.ft.Text("Arquivo de Gases (CSV)", color=self.ft.Colors.WHITE),
                        subtitle=self.txt_gases,
                        trailing=self.ft.ElevatedButton(
                            "Procurar...", 
                            icon=self.ft.Icons.FOLDER_OPEN,
                            on_click=lambda _: self.picker_gases.pick_files(allow_multiple=False, allowed_extensions=["csv"])
                        )
                    ),
                    # Seletor do arquivo de movimento
                    self.ft.ListTile(
                        leading=self.ft.Icon(self.ft.Icons.EDV_SHRINK_VIEW, color=self.ft.Colors.WHITE),
                        title=self.ft.Text("Arquivo de Movimento (CSV)", color=self.ft.Colors.WHITE),
                        subtitle=self.txt_movimento,
                        trailing=self.ft.ElevatedButton(
                            "Procurar...", 
                            icon=self.ft.Icons.FOLDER_OPEN,
                            on_click=lambda _: self.picker_movimento.pick_files(allow_multiple=False, allowed_extensions=["csv"])
                        )
                    ),
                    # Botão de envio processado em Lote
                    self.ft.Container(
                        content=self.ft.Column([
                            self.ft.ElevatedButton(
                                "Mesclar e Enviar Telemetria",
                                icon=self.ft.Icons.UPLOAD_FILE,
                                bgcolor=self.ft.Colors.BLUE_600,
                                color=self.ft.Colors.WHITE,
                                on_click=self._disparar_importacao,
                                width=250
                            ),
                            self.txt_status
                        ], alignment=self.ft.MainAxisAlignment.CENTER, horizontal_alignment=self.ft.CrossAxisAlignment.CENTER),
                        padding=15,
                        alignment=self.ft.alignment.center
                    )
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
                    ),
                    self.ft.ListTile(
                        leading=self.ft.Icon(self.ft.Icons.LOGOUT, color=self.ft.Colors.RED_400),
                        title=self.ft.Text("Sair da Conta", color=self.ft.Colors.RED_400),
                    ),
                ]),
                bgcolor="#111827",
                border_radius=10,
                padding=10
            ),

        ], expand=True, scroll=self.ft.ScrollMode.AUTO)