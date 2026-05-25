

class ProfileSelectionView:
    def __init__(self, system):
        self.system = system
        self.on_profile_selected = self.system.view.page.home
        self.ft = self.system.ft

    def render(self):
        self.system.page.clean()
        self.system.page.padding = 0

        # Fundo global da tela (Gradiente Escuro Roxo/Azul estilo HBO)
        fundo_gradiente = self.ft.RadialGradient(
            colors=["#2A0A4A", "#050011"], 
            center=self.ft.alignment.top_center, 
            radius=1.5
        )

        def voltar_para_selecao():
            """Função de callback passada para as outras views retornarem ao menu."""
            trocar_tela(build_selection_view())

        # --- CONSTRUTOR DA TELA INICIAL (BOLHAS) ---
        def build_selection_view():
            titulo = self.ft.Text("Quem está monitorando?", size=40, weight=self.ft.FontWeight.W_300, color=self.ft.Colors.WHITE)

            # Botão de Engrenagem (Configurações Globais) no topo
            btn_engrenagem = self.ft.Container(
                content=self.ft.IconButton(
                    icon=self.ft.Icons.SETTINGS,
                    icon_color=self.ft.Colors.GREY_400,
                    icon_size=28,
                    tooltip="Configurações Globais",
                    # Instancia a classe separada de Configurações
                    on_click=lambda e: trocar_tela(GlobalSettingsView(self.system, voltar_para_selecao).build())
                ),
                alignment=self.ft.alignment.top_right,
                padding=self.ft.padding.only(top=20, right=40)
            )

            def criar_bolha_perfil(nome, gradiente_colors, is_add_button=False):
                letra_inicial = nome[0].upper() if not is_add_button else "+"
                
                circulo_interno = self.ft.Container(
                    width=132, height=132, shape=self.ft.BoxShape.CIRCLE, bgcolor="#050011",
                    content=self.ft.Text(letra_inicial, size=50, weight=self.ft.FontWeight.W_200, color=self.ft.Colors.WHITE),
                    alignment=self.ft.alignment.center,
                )

                circulo_externo = self.ft.Container(
                    width=140, height=140, shape=self.ft.BoxShape.CIRCLE,
                    gradient=self.ft.LinearGradient(
                        begin=self.ft.alignment.top_left, end=self.ft.alignment.bottom_right, colors=gradiente_colors
                    ) if not is_add_button else None,
                    border=self.ft.border.all(2, self.ft.Colors.GREY_700) if is_add_button else None,
                    content=circulo_interno,
                    alignment=self.ft.alignment.center,
                    animate_scale=self.ft.Animation(200, self.ft.AnimationCurve.DECELERATE),
                )

                nome_texto = self.ft.Text(nome, size=16, color=self.ft.Colors.GREY_400, weight=self.ft.FontWeight.W_400)

                lapis_icon = self.ft.IconButton(
                    icon=self.ft.Icons.EDIT, icon_color=self.ft.Colors.GREY_600, icon_size=16,
                    # Instancia a classe separada de Edição
                    on_click=lambda e: trocar_tela(ProfileEditView(self.system, nome, gradiente_colors, voltar_para_selecao).build()),
                    visible=not is_add_button
                )

                def on_hover(e):
                    if e.data == "true":
                        circulo_externo.scale = 1.1
                        nome_texto.color = self.ft.Colors.WHITE
                    else:
                        circulo_externo.scale = 1.0
                        nome_texto.color = self.ft.Colors.GREY_400
                    circulo_externo.update()
                    nome_texto.update()

                def on_click_action(e):
                    if is_add_button:
                        # Instancia a classe separada para Novo Perfil
                        trocar_tela(ProfileEditView(self.system, "Novo Perfil", ["#4364F7", "#6FB1FC"], voltar_para_selecao).build())
                    else:
                        self.on_profile_selected(self.system).render()

                return self.ft.Container(
                    content=self.ft.Column(
                        [
                            circulo_externo,
                            self.ft.Container(height=10),
                            self.ft.Row([nome_texto, lapis_icon], alignment=self.ft.MainAxisAlignment.CENTER, spacing=0)
                        ],
                        horizontal_alignment=self.ft.CrossAxisAlignment.CENTER, spacing=0
                    ),
                    on_hover=on_hover, on_click=on_click_action
                )

            grid_perfis = self.ft.Row(
                [
                    criar_bolha_perfil("Maquinhos", ["#FF007F", "#7F00FF"]), 
                    criar_bolha_perfil("Rodinha", ["#0052D4", "#6FB1FC"]),   
                    criar_bolha_perfil("Adicionar", [], is_add_button=True)
                ],
                alignment=self.ft.MainAxisAlignment.CENTER, spacing=50
            )

            return self.ft.Column(
                [
                    btn_engrenagem,
                    self.ft.Container(height=40),
                    titulo,
                    self.ft.Container(height=60),
                    grid_perfis,
                ],
                horizontal_alignment=self.ft.CrossAxisAlignment.CENTER, expand=True
            )

        # --- GERENCIADOR DE ESTADO (TROCA DE TELAS) ---
        self.main_content = self.ft.Container(
            content=build_selection_view(), 
            expand=True,
            gradient=fundo_gradiente,
            opacity=0,
            animate_opacity=800,
        )

        def trocar_tela(nova_view):
            self.main_content.opacity = 0
            self.main_content.update()
            time.sleep(0.3)
            self.main_content.content = nova_view
            self.main_content.opacity = 1
            self.main_content.update()

        self.system.page.add(self.main_content)
        
        # Disparo da Animação Inicial
        self.system.time.sleep(0.1)
        self.main_content.opacity = 1
        self.main_content.update()