import time

class CadastroCarrinhoView:
    def __init__(self, system):
        self.system = system
        self.on_back_to_profile = self.system.view.page.profileSelection
        self.ft = self.system.ft

    def render(self):
        self.system.page.clean()
        self.system.page.padding = 0

        # --- FUNÇÕES SECUNDÁRIAS ---
        def fechar_popup(dlg):
            dlg.open = False
            self.system.page.update()

        def voltar_click(e):
            self.on_back_to_profile(self.system).render()

        def handle_cadastro_carrinho(e):
            """Valida e cadastra um novo carrinho."""
            nome = input_nome.value
            codigo = input_codigo.value
            
            # Validação básica
            if not nome or not codigo:
                dlg = self.ft.AlertDialog(
                    title=self.ft.Text("Atenção", weight=self.ft.FontWeight.BOLD),
                    content=self.ft.Text("Por favor, preencha todos os campos."),
                    actions=[
                        self.ft.TextButton("OK", on_click=lambda e: fechar_popup(dlg))
                    ],
                    shape=self.ft.RoundedRectangleBorder(radius=15),
                )
                self.system.page.dialog = dlg
                dlg.open = True
                self.system.page.update()
                return
            
            # Tenta cadastrar o carrinho no banco de dados
            id_usuario = self.system.obter_id_usuario()
            novo_carrinho = self.system.model.database.cadastrar_carrinho(
                nome=nome,
                codigo=codigo,
                id_usuario=id_usuario
            )
            
            if novo_carrinho:
                # Mostra sucesso
                dlg = self.ft.AlertDialog(
                    title=self.ft.Text("Carrinho Cadastrado", weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.GREEN_400),
                    content=self.ft.Text(f"O carrinho '{nome}' foi cadastrado com sucesso!"),
                    actions=[
                        self.ft.TextButton("OK", on_click=lambda e: (fechar_popup(dlg), self.on_back_to_profile(self.system).render()))
                    ],
                    shape=self.ft.RoundedRectangleBorder(radius=15),
                    bgcolor="#15171E"
                )
                self.system.page.dialog = dlg
                dlg.open = True
                self.system.page.update()
            else:
                # Mostra erro
                dlg = self.ft.AlertDialog(
                    title=self.ft.Text("Erro no Cadastro", weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.RED_400),
                    content=self.ft.Text("Não foi possível cadastrar o carrinho. Tente novamente."),
                    actions=[
                        self.ft.TextButton("OK", on_click=lambda e: fechar_popup(dlg))
                    ],
                    shape=self.ft.RoundedRectangleBorder(radius=15),
                    bgcolor="#15171E"
                )
                self.system.page.dialog = dlg
                dlg.open = True
                self.system.page.update()

        # --- CONSTRUÇÃO DA UI (LADO ESQUERDO) ---
        titulo = self.ft.Text("Cadastrar Novo Carrinho", size=40, weight=self.ft.FontWeight.W_900, color=self.ft.Colors.WHITE)
        subtitulo = self.ft.Text("Preencha os dados do carrinho abaixo.", size=14, color=self.ft.Colors.GREY_500)
        
        # Campos de Entrada 
        input_nome = self.ft.TextField(
            label="Nome do Carrinho", 
            width=350, 
            prefix_icon=self.ft.Icons.DIRECTIONS_CAR,
            border_radius=8,
            border_color=self.ft.Colors.TRANSPARENT,
            filled=True,
            bgcolor="#15171E",
            color=self.ft.Colors.WHITE
        )

        input_codigo = self.ft.TextField(
            label="Código do Carrinho", 
            width=350, 
            prefix_icon=self.ft.Icons.QR_CODE,
            border_radius=8,
            border_color=self.ft.Colors.TRANSPARENT,
            filled=True,
            bgcolor="#15171E",
            color=self.ft.Colors.WHITE
        )

        # Botão Principal com Gradiente Verde
        btn_cadastro = self.ft.Container(
            content=self.ft.Text("Cadastrar", size=16, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            alignment=self.ft.alignment.center,
            width=350,
            height=50,
            border_radius=25,
            ink=True,
            on_click=handle_cadastro_carrinho,
            gradient=self.ft.LinearGradient(
                begin=self.ft.alignment.center_left,
                end=self.ft.alignment.center_right,
                colors=["#00C851", "#33B5FF"]  # Verde para Azul
            ),
            shadow=self.ft.BoxShadow(spread_radius=1, blur_radius=15, color="#00C851", offset=self.ft.Offset(0, 5))
        )

        # Botão Voltar
        btn_voltar = self.ft.Container(
            content=self.ft.TextButton("← Voltar", on_click=voltar_click, style=self.ft.ButtonStyle(color=self.ft.Colors.GREY_500)),
            margin=self.ft.margin.only(top=20)
        )

        # Agrupando o formulário
        form_column = self.ft.Column(
            [
                titulo,
                subtitulo,
                self.ft.Container(height=40),
                input_nome,
                self.ft.Container(height=15),
                input_codigo,
                self.ft.Container(height=30),
                btn_cadastro,
                btn_voltar
            ],
            alignment=self.ft.MainAxisAlignment.CENTER,
            horizontal_alignment=self.ft.CrossAxisAlignment.START,
        )

        # Painel Esquerdo (Preto)
        left_panel = self.ft.Container(
            content=form_column,
            width=500,
            padding=self.ft.padding.only(left=80, right=40),
            bgcolor="#0A0B10",
            alignment=self.ft.alignment.center,
            
            # Animação de entrada
            opacity=0, 
            offset=self.ft.Offset(-0.2, 0),
            animate_opacity=700, 
            animate_offset=self.ft.Animation(700, self.ft.AnimationCurve.EASE_OUT_EXPO)
        )

        # Painel Direito (Imagem)
        right_panel = self.ft.Container(
            expand=True,
            image=self.ft.DecorationImage(
                src="assets/carrinho_ft_01.jpg",
                fit=self.ft.ImageFit.COVER
            )
        )

        # Layout Principal
        layout = self.ft.Row(
            controls=[left_panel, right_panel],
            expand=True,
            spacing=0
        )
        
        self.system.page.add(layout)
        
        # --- DISPARO DA ANIMAÇÃO ---
        time.sleep(0.1) 
        left_panel.opacity = 1
        left_panel.offset = self.ft.Offset(0, 0)
        left_panel.update()
