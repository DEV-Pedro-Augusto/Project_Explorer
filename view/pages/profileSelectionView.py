import flet as ft
import time

class ProfileSelectionView:
    def __init__(self, page: ft.Page, on_profile_selected):
        self.page = page
        self.on_profile_selected = on_profile_selected

    def render(self):
        self.page.clean()
        self.page.padding = 0

        # Fundo global da tela (Gradiente Escuro Roxo/Azul estilo HBO)
        fundo_gradiente = ft.RadialGradient(
            colors=["#2A0A4A", "#050011"], 
            center=ft.alignment.top_center, 
            radius=1.5
        )

        # --- CONSTRUTORES DE TELAS INTERNAS ---

        def build_selection_view():
            """Constrói a tela inicial com as bolhas dos perfis."""
            titulo = ft.Text("Quem está monitorando?", size=40, weight=ft.FontWeight.W_300, color=ft.Colors.WHITE)

            # Botão de Engrenagem (Configurações Globais) no topo
            btn_engrenagem = ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.SETTINGS,
                    icon_color=ft.Colors.GREY_400,
                    icon_size=28,
                    tooltip="Configurações Globais",
                    on_click=lambda e: trocar_tela(build_global_settings_view())
                ),
                alignment=ft.alignment.top_right,
                padding=ft.padding.only(top=20, right=40)
            )

            def criar_bolha_perfil(nome, gradiente_colors, is_add_button=False):
                letra_inicial = nome[0].upper() if not is_add_button else "+"
                
                # Círculo central (Preto) que vai por cima do gradiente para dar efeito de borda
                circulo_interno = ft.Container(
                    width=132, height=132,
                    shape=ft.BoxShape.CIRCLE,
                    bgcolor="#050011",
                    content=ft.Text(letra_inicial, size=50, weight=ft.FontWeight.W_200, color=ft.Colors.WHITE),
                    alignment=ft.alignment.center,
                )

                # Círculo externo (Gradiente)
                circulo_externo = ft.Container(
                    width=140, height=140,
                    shape=ft.BoxShape.CIRCLE,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left, end=ft.alignment.bottom_right,
                        colors=gradiente_colors
                    ) if not is_add_button else None,
                    border=ft.border.all(2, ft.Colors.GREY_700) if is_add_button else None,
                    content=circulo_interno,
                    alignment=ft.alignment.center,
                    animate_scale=ft.Animation(200, ft.AnimationCurve.DECELERATE),
                )

                nome_texto = ft.Text(nome, size=16, color=ft.Colors.GREY_400, weight=ft.FontWeight.W_400)

                lapis_icon = ft.IconButton(
                    icon=ft.Icons.EDIT, icon_color=ft.Colors.GREY_600, icon_size=16,
                    on_click=lambda e: trocar_tela(build_edit_view(nome, gradiente_colors)),
                    visible=not is_add_button
                )

                def on_hover(e):
                    if e.data == "true":
                        circulo_externo.scale = 1.1
                        nome_texto.color = ft.Colors.WHITE
                    else:
                        circulo_externo.scale = 1.0
                        nome_texto.color = ft.Colors.GREY_400
                    circulo_externo.update()
                    nome_texto.update()

                def on_click_action(e):
                    if is_add_button:
                        trocar_tela(build_edit_view("Novo Perfil", ["#4364F7", "#6FB1FC"]))
                    else:
                        self.on_profile_selected(nome)

                return ft.Container(
                    content=ft.Column(
                        [
                            circulo_externo,
                            ft.Container(height=10),
                            ft.Row([nome_texto, lapis_icon], alignment=ft.MainAxisAlignment.CENTER, spacing=0)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0
                    ),
                    on_hover=on_hover, on_click=on_click_action
                )

            grid_perfis = ft.Row(
                [
                    criar_bolha_perfil("Maquinhos", ["#FF007F", "#7F00FF"]), 
                    criar_bolha_perfil("Rodinha", ["#0052D4", "#6FB1FC"]),   
                    criar_bolha_perfil("Adicionar", [], is_add_button=True)
                ],
                alignment=ft.MainAxisAlignment.CENTER, spacing=50
            )

            return ft.Column(
                [
                    btn_engrenagem,
                    ft.Container(height=40),
                    titulo,
                    ft.Container(height=60),
                    grid_perfis,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True
            )

        def build_global_settings_view():
            """Constrói a tela de Configurações Globais (Rede e Tema)."""
            titulo = ft.Text("Configurações Globais", size=36, weight=ft.FontWeight.W_300, color=ft.Colors.WHITE)

            # Lado Esquerdo (Ícone de Rede brilhante)
            icone_rede = ft.Container(
                width=160, height=160, shape=ft.BoxShape.CIRCLE,
                gradient=ft.LinearGradient(colors=["#0052D4", "#7F00FF"]),
                content=ft.Container(
                    width=150, height=150, shape=ft.BoxShape.CIRCLE, bgcolor="#050011",
                    content=ft.Icon(ft.Icons.ROUTER, size=70, color=ft.Colors.GREY_400),
                    alignment=ft.alignment.center
                ),
                alignment=ft.alignment.center
            )

            caixa_info = ft.Container(
                content=ft.Text("Estas configurações\nserão aplicadas como\npadrão para os robôs.", text_align=ft.TextAlign.CENTER, size=12, color=ft.Colors.GREY_400),
                padding=20, bgcolor="#151125", border_radius=15, width=180
            )

            col_esquerda = ft.Column([icone_rede, ft.Container(height=20), caixa_info], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            # Lado Direito (Formulário)
            input_rede = ft.TextField(
                label="Nome da Rede Wi-Fi (SSID)", 
                width=350, border=ft.InputBorder.UNDERLINE, color=ft.Colors.WHITE, bgcolor=ft.Colors.TRANSPARENT,
                prefix_icon=ft.Icons.WIFI
            )

            input_senha = ft.TextField(
                label="Senha da Rede", 
                width=350, border=ft.InputBorder.UNDERLINE, color=ft.Colors.WHITE, bgcolor=ft.Colors.TRANSPARENT,
                password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK_OUTLINE
            )

            # Seletor de Tema
            texto_tema = ft.Text("Tema Básico do App", color=ft.Colors.GREY_400, size=14)
            
            def criar_botao_tema(nome, icone, cor_ativa):
                return ft.Container(
                    content=ft.Row([ft.Icon(icone, size=18, color=ft.Colors.WHITE), ft.Text(nome, color=ft.Colors.WHITE)]),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    border_radius=20,
                    bgcolor=cor_ativa,
                    ink=True,
                    on_click=lambda e: print(f"Tema {nome} selecionado!")
                )

            paleta_temas = ft.Row([
                criar_botao_tema("Escuro", ft.Icons.DARK_MODE, "#2A2A35"), # Tema ativo (exemplo)
                criar_botao_tema("Claro", ft.Icons.LIGHT_MODE, ft.Colors.TRANSPARENT)
            ], spacing=15)

            col_direita = ft.Column(
                [
                    ft.Container(height=20), 
                    input_rede, 
                    ft.Container(height=20), 
                    input_senha, 
                    ft.Container(height=30), 
                    texto_tema,
                    ft.Container(height=5),
                    paleta_temas
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.START
            )

            # Botões inferiores
            btn_salvar = ft.Container(
                content=ft.Text("SALVAR", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                alignment=ft.alignment.center, width=150, height=45, border_radius=25, ink=True,
                gradient=ft.LinearGradient(colors=["#7F00FF", "#0052D4"]),
                on_click=lambda e: trocar_tela(build_selection_view()) 
            )

            btn_cancelar = ft.Container(
                content=ft.Text("CANCELAR", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300),
                alignment=ft.alignment.center, width=150, height=45, border_radius=25, bgcolor="#2A2A35", ink=True,
                on_click=lambda e: trocar_tela(build_selection_view()) 
            )

            botoes_acao = ft.Row([btn_salvar, btn_cancelar], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

            return ft.Column(
                [
                    ft.Container(height=60),
                    titulo,
                    ft.Container(height=50),
                    ft.Row([col_esquerda, ft.Container(width=50), col_direita], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),
                    ft.Container(height=60),
                    botoes_acao
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True
            )

        def build_edit_view(nome_atual, cor_atual):
            """Constrói a tela de criar/editar perfil."""
            titulo = ft.Text("Criar perfil" if nome_atual == "Novo Perfil" else "Editar perfil", size=36, weight=ft.FontWeight.W_300, color=ft.Colors.WHITE)

            # Lado Esquerdo (Avatar)
            avatar_preview = ft.Container(
                width=160, height=160, shape=ft.BoxShape.CIRCLE,
                gradient=ft.LinearGradient(colors=cor_atual),
                content=ft.Container(
                    width=150, height=150, shape=ft.BoxShape.CIRCLE, bgcolor="#050011",
                    content=ft.Icon(ft.Icons.PERSON_OUTLINE, size=80, color=ft.Colors.GREY_400),
                    alignment=ft.alignment.center
                ),
                alignment=ft.alignment.center
            )

            caixa_foto = ft.Container(
                content=ft.Text("Use o aplicativo para\ncarregar uma foto ou\nescolher um avatar.", text_align=ft.TextAlign.CENTER, size=12, color=ft.Colors.GREY_400),
                padding=20, bgcolor="#151125", border_radius=15, width=180
            )

            col_esquerda = ft.Column([avatar_preview, ft.Container(height=20), caixa_foto], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            # Lado Direito (Formulário)
            input_nome = ft.TextField(
                label="Nome", value="" if nome_atual == "Novo Perfil" else nome_atual,
                width=350, border=ft.InputBorder.UNDERLINE, color=ft.Colors.WHITE, bgcolor=ft.Colors.TRANSPARENT
            )

            def criar_bolinha_cor(cores):
                return ft.Container(
                    width=40, height=40, shape=ft.BoxShape.CIRCLE,
                    gradient=ft.LinearGradient(colors=cores), ink=True,
                    on_click=lambda e: print(f"Cor selecionada!") 
                )

            paleta_cores = ft.Row([
                criar_bolinha_cor(["#FF007F", "#FF007F"]), 
                criar_bolinha_cor(["#FF007F", "#7F00FF"]), 
                criar_bolinha_cor(["#7F00FF", "#7F00FF"]), 
                criar_bolinha_cor(["#0052D4", "#7F00FF"]), 
                criar_bolinha_cor(["#0052D4", "#6FB1FC"]), 
            ], spacing=15)

            col_direita = ft.Column([ft.Container(height=40), input_nome, ft.Container(height=40), paleta_cores], horizontal_alignment=ft.CrossAxisAlignment.START)

            # Botões inferiores
            btn_salvar = ft.Container(
                content=ft.Text("SALVAR", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                alignment=ft.alignment.center, width=150, height=45, border_radius=25, ink=True,
                gradient=ft.LinearGradient(colors=["#7F00FF", "#0052D4"]),
                on_click=lambda e: trocar_tela(build_selection_view()) 
            )

            btn_cancelar = ft.Container(
                content=ft.Text("CANCELAR", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300),
                alignment=ft.alignment.center, width=150, height=45, border_radius=25, bgcolor="#2A2A35", ink=True,
                on_click=lambda e: trocar_tela(build_selection_view()) 
            )

            botoes_acao = ft.Row([btn_salvar, btn_cancelar], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

            return ft.Column(
                [
                    ft.Container(height=60),
                    titulo,
                    ft.Container(height=50),
                    ft.Row([col_esquerda, ft.Container(width=50), col_direita], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),
                    ft.Container(height=60),
                    botoes_acao
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True
            )

        # --- GERENCIADOR DE ESTADO (TROCA DE TELAS) ---

        self.main_content = ft.Container(
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

        self.page.add(self.main_content)
        
        # Disparo da Animação Inicial
        time.sleep(0.1)
        self.main_content.opacity = 1
        self.main_content.update()