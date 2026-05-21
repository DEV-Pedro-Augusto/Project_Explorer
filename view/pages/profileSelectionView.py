import flet as ft
import time

class ProfileSelectionView:
    def __init__(self, system ):
        self.system = system
        self.on_profile_selected = self.system.view.page.home
        self.ft = self.system.ft

    def render(self):
        self.system.page.clean()
        self.system.page.padding = 0

        # Fundo global da tela (Gradiente Escuro Roxo/Azul estilo HBO)
        fundo_gradiente =self.ft.RadialGradient(
            colors=["#2A0A4A", "#050011"], 
            center=self.system.ft.alignment.top_center, 
            radius=1.5
        )

        # --- CONSTRUTORES DE TELAS INTERNAS ---

        def build_selection_view():
            """Constrói a tela inicial com as bolhas dos perfis."""
            titulo =self.ft.Text("Quem está monitorando?", size=40, weight=self.system.ft.FontWeight.W_300, color=self.system.ft.Colors.WHITE)

            # Botão de Engrenagem (Configurações Globais) no topo
            btn_engrenagem =self.ft.Container(
                content=self.system.ft.IconButton(
                    icon=self.system.ft.Icons.SETTINGS,
                    icon_color=self.system.ft.Colors.GREY_400,
                    icon_size=28,
                    tooltip="Configurações Globais",
                    on_click=lambda e: trocar_tela(build_global_settings_view())
                ),
                alignment=self.system.ft.alignment.top_right,
                padding=self.system.ft.padding.only(top=20, right=40)
            )

            def criar_bolha_perfil(nome, gradiente_colors, is_add_button=False):
                letra_inicial = nome[0].upper() if not is_add_button else "+"
                
                # Círculo central (Preto) que vai por cima do gradiente para dar efeito de borda
                circulo_interno =self.ft.Container(
                    width=132, height=132,
                    shape=self.system.ft.BoxShape.CIRCLE,
                    bgcolor="#050011",
                    content=self.system.ft.Text(letra_inicial, size=50, weight=self.system.ft.FontWeight.W_200, color=self.system.ft.Colors.WHITE),
                    alignment=self.system.ft.alignment.center,
                )

                # Círculo externo (Gradiente)
                circulo_externo =self.ft.Container(
                    width=140, height=140,
                    shape=self.system.ft.BoxShape.CIRCLE,
                    gradient=self.system.ft.LinearGradient(
                        begin=self.system.ft.alignment.top_left, end=self.system.ft.alignment.bottom_right,
                        colors=gradiente_colors
                    ) if not is_add_button else None,
                    border=self.system.ft.border.all(2,self.ft.Colors.GREY_700) if is_add_button else None,
                    content=circulo_interno,
                    alignment=self.system.ft.alignment.center,
                    animate_scale=self.system.ft.Animation(200,self.ft.AnimationCurve.DECELERATE),
                )

                nome_texto =self.ft.Text(nome, size=16, color=self.system.ft.Colors.GREY_400, weight=self.system.ft.FontWeight.W_400)

                lapis_icon =self.ft.IconButton(
                    icon=self.system.ft.Icons.EDIT, icon_color=self.system.ft.Colors.GREY_600, icon_size=16,
                    on_click=lambda e: trocar_tela(build_edit_view(nome, gradiente_colors)),
                    visible=not is_add_button
                )

                def on_hover(e):
                    if e.data == "true":
                        circulo_externo.scale = 1.1
                        nome_texto.color =self.ft.Colors.WHITE
                    else:
                        circulo_externo.scale = 1.0
                        nome_texto.color =self.ft.Colors.GREY_400
                    circulo_externo.update()
                    nome_texto.update()

                def on_click_action(e):
                    if is_add_button:
                        trocar_tela(build_edit_view("Novo Perfil", ["#4364F7", "#6FB1FC"]))
                    else:
                        self.on_profile_selected(self.system).render()

                return self.ft.Container(
                    content=self.system.ft.Column(
                        [
                            circulo_externo,
                           self.ft.Container(height=10),
                           self.ft.Row([nome_texto, lapis_icon], alignment=self.system.ft.MainAxisAlignment.CENTER, spacing=0)
                        ],
                        horizontal_alignment=self.system.ft.CrossAxisAlignment.CENTER, spacing=0
                    ),
                    on_hover=on_hover, on_click=on_click_action
                )

            grid_perfis =self.ft.Row(
                [
                    criar_bolha_perfil("Maquinhos", ["#FF007F", "#7F00FF"]), 
                    criar_bolha_perfil("Rodinha", ["#0052D4", "#6FB1FC"]),   
                    criar_bolha_perfil("Adicionar", [], is_add_button=True)
                ],
                alignment=self.system.ft.MainAxisAlignment.CENTER, spacing=50
            )

            return self.ft.Column(
                [
                    btn_engrenagem,
                   self.ft.Container(height=40),
                    titulo,
                   self.ft.Container(height=60),
                    grid_perfis,
                ],
                horizontal_alignment=self.system.ft.CrossAxisAlignment.CENTER, expand=True
            )

        def build_global_settings_view():
            """Constrói a tela de Configurações Globais (Rede e Tema)."""
            titulo =self.ft.Text("Configurações Globais", size=36, weight=self.system.ft.FontWeight.W_300, color=self.system.ft.Colors.WHITE)

            # Lado Esquerdo (Ícone de Rede brilhante)
            icone_rede =self.ft.Container(
                width=160, height=160, shape=self.system.ft.BoxShape.CIRCLE,
                gradient=self.system.ft.LinearGradient(colors=["#0052D4", "#7F00FF"]),
                content=self.system.ft.Container(
                    width=150, height=150, shape=self.system.ft.BoxShape.CIRCLE, bgcolor="#050011",
                    content=self.system.ft.Icon(self.system.ft.Icons.ROUTER, size=70, color=self.system.ft.Colors.GREY_400),
                    alignment=self.system.ft.alignment.center
                ),
                alignment=self.system.ft.alignment.center
            )

            caixa_info =self.ft.Container(
                content=self.system.ft.Text("Estas configurações\nserão aplicadas como\npadrão para os robôs.", text_align=self.system.ft.TextAlign.CENTER, size=12, color=self.system.ft.Colors.GREY_400),
                padding=20, bgcolor="#151125", border_radius=15, width=180
            )

            col_esquerda =self.ft.Column([icone_rede,self.ft.Container(height=20), caixa_info], horizontal_alignment=self.system.ft.CrossAxisAlignment.CENTER)

            # Lado Direito (Formulário)
            input_rede =self.ft.TextField(
                label="Nome da Rede Wi-Fi (SSID)", 
                width=350, border=self.system.ft.InputBorder.UNDERLINE, color=self.system.ft.Colors.WHITE, bgcolor=self.system.ft.Colors.TRANSPARENT,
                prefix_icon=self.system.ft.Icons.WIFI
            )

            input_senha =self.ft.TextField(
                label="Senha da Rede", 
                width=350, border=self.system.ft.InputBorder.UNDERLINE, color=self.system.ft.Colors.WHITE, bgcolor=self.system.ft.Colors.TRANSPARENT,
                password=True, can_reveal_password=True, prefix_icon=self.system.ft.Icons.LOCK_OUTLINE
            )

            # Seletor de Tema
            texto_tema =self.ft.Text("Tema Básico do App", color=self.system.ft.Colors.GREY_400, size=14)
            
            def criar_botao_tema(nome, icone, cor_ativa):
                return self.ft.Container(
                    content=self.system.ft.Row([self.system.ft.Icon(icone, size=18, color=self.system.ft.Colors.WHITE),self.ft.Text(nome, color=self.system.ft.Colors.WHITE)]),
                    padding=self.system.ft.padding.symmetric(horizontal=20, vertical=10),
                    border_radius=20,
                    bgcolor=cor_ativa,
                    ink=True,
                    on_click=lambda e: print(f"Tema {nome} selecionado!")
                )

            paleta_temas =self.ft.Row([
                criar_botao_tema("Escuro",self.ft.Icons.DARK_MODE, "#2A2A35"), # Tema ativo (exemplo)
                criar_botao_tema("Claro",self.ft.Icons.LIGHT_MODE,self.ft.Colors.TRANSPARENT)
            ], spacing=15)

            col_direita =self.ft.Column(
                [
                   self.ft.Container(height=20), 
                    input_rede, 
                   self.ft.Container(height=20), 
                    input_senha, 
                   self.ft.Container(height=30), 
                    texto_tema,
                   self.ft.Container(height=5),
                    paleta_temas
                ], 
                horizontal_alignment=self.system.ft.CrossAxisAlignment.START
            )

            # Botões inferiores
            btn_salvar =self.ft.Container(
                content=self.system.ft.Text("SALVAR", weight=self.system.ft.FontWeight.BOLD, color=self.system.ft.Colors.WHITE),
                alignment=self.system.ft.alignment.center, width=150, height=45, border_radius=25, ink=True,
                gradient=self.system.ft.LinearGradient(colors=["#7F00FF", "#0052D4"]),
                on_click=lambda e: trocar_tela(build_selection_view()) 
            )

            btn_cancelar =self.ft.Container(
                content=self.system.ft.Text("CANCELAR", weight=self.system.ft.FontWeight.BOLD, color=self.system.ft.Colors.GREY_300),
                alignment=self.system.ft.alignment.center, width=150, height=45, border_radius=25, bgcolor="#2A2A35", ink=True,
                on_click=lambda e: trocar_tela(build_selection_view()) 
            )

            botoes_acao =self.ft.Row([btn_salvar, btn_cancelar], alignment=self.system.ft.MainAxisAlignment.CENTER, spacing=20)

            return self.ft.Column(
                [
                   self.ft.Container(height=60),
                    titulo,
                   self.ft.Container(height=50),
                   self.ft.Row([col_esquerda,self.ft.Container(width=50), col_direita], alignment=self.system.ft.MainAxisAlignment.CENTER, vertical_alignment=self.system.ft.CrossAxisAlignment.START),
                   self.ft.Container(height=60),
                    botoes_acao
                ],
                horizontal_alignment=self.system.ft.CrossAxisAlignment.CENTER, expand=True
            )

        def build_edit_view(nome_atual, cor_atual):
            """Constrói a tela de criar/editar perfil."""
            titulo =self.ft.Text("Criar perfil" if nome_atual == "Novo Perfil" else "Editar perfil", size=36, weight=self.system.ft.FontWeight.W_300, color=self.system.ft.Colors.WHITE)

            # Lado Esquerdo (Avatar)
            avatar_preview =self.ft.Container(
                width=160, height=160, shape=self.system.ft.BoxShape.CIRCLE,
                gradient=self.system.ft.LinearGradient(colors=cor_atual),
                content=self.system.ft.Container(
                    width=150, height=150, shape=self.system.ft.BoxShape.CIRCLE, bgcolor="#050011",
                    content=self.system.ft.Icon(self.system.ft.Icons.PERSON_OUTLINE, size=80, color=self.system.ft.Colors.GREY_400),
                    alignment=self.system.ft.alignment.center
                ),
                alignment=self.system.ft.alignment.center
            )

            caixa_foto =self.ft.Container(
                content=self.system.ft.Text("Use o aplicativo para\ncarregar uma foto ou\nescolher um avatar.", text_align=self.system.ft.TextAlign.CENTER, size=12, color=self.system.ft.Colors.GREY_400),
                padding=20, bgcolor="#151125", border_radius=15, width=180
            )

            col_esquerda =self.ft.Column([avatar_preview,self.ft.Container(height=20), caixa_foto], horizontal_alignment=self.system.ft.CrossAxisAlignment.CENTER)

            # Lado Direito (Formulário)
            input_nome =self.ft.TextField(
                label="Nome", value="" if nome_atual == "Novo Perfil" else nome_atual,
                width=350, border=self.system.ft.InputBorder.UNDERLINE, color=self.system.ft.Colors.WHITE, bgcolor=self.system.ft.Colors.TRANSPARENT
            )

            def criar_bolinha_cor(cores):
                return self.ft.Container(
                    width=40, height=40, shape=self.system.ft.BoxShape.CIRCLE,
                    gradient=self.system.ft.LinearGradient(colors=cores), ink=True,
                    on_click=lambda e: print(f"Cor selecionada!") 
                )

            paleta_cores =self.ft.Row([
                criar_bolinha_cor(["#FF007F", "#FF007F"]), 
                criar_bolinha_cor(["#FF007F", "#7F00FF"]), 
                criar_bolinha_cor(["#7F00FF", "#7F00FF"]), 
                criar_bolinha_cor(["#0052D4", "#7F00FF"]), 
                criar_bolinha_cor(["#0052D4", "#6FB1FC"]), 
            ], spacing=15)

            col_direita =self.ft.Column([self.system.ft.Container(height=40), input_nome,self.ft.Container(height=40), paleta_cores], horizontal_alignment=self.system.ft.CrossAxisAlignment.START)

            # Botões inferiores
            btn_salvar =self.ft.Container(
                content=self.system.ft.Text("SALVAR", weight=self.system.ft.FontWeight.BOLD, color=self.system.ft.Colors.WHITE),
                alignment=self.system.ft.alignment.center, width=150, height=45, border_radius=25, ink=True,
                gradient=self.system.ft.LinearGradient(colors=["#7F00FF", "#0052D4"]),
                on_click=lambda e: trocar_tela(build_selection_view()) 
            )

            btn_cancelar =self.ft.Container(
                content=self.system.ft.Text("CANCELAR", weight=self.system.ft.FontWeight.BOLD, color=self.system.ft.Colors.GREY_300),
                alignment=self.system.ft.alignment.center, width=150, height=45, border_radius=25, bgcolor="#2A2A35", ink=True,
                on_click=lambda e: trocar_tela(build_selection_view()) 
            )

            botoes_acao =self.ft.Row([btn_salvar, btn_cancelar], alignment=self.system.ft.MainAxisAlignment.CENTER, spacing=20)

            return self.ft.Column(
                [
                   self.ft.Container(height=60),
                    titulo,
                   self.ft.Container(height=50),
                   self.ft.Row([col_esquerda,self.ft.Container(width=50), col_direita], alignment=self.system.ft.MainAxisAlignment.CENTER, vertical_alignment=self.system.ft.CrossAxisAlignment.START),
                   self.ft.Container(height=60),
                    botoes_acao
                ],
                horizontal_alignment=self.system.ft.CrossAxisAlignment.CENTER, expand=True
            )

        # --- GERENCIADOR DE ESTADO (TROCA DE TELAS) ---

        self.main_content =self.ft.Container(
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
        time.sleep(0.1)
        self.main_content.opacity = 1
        self.main_content.update()