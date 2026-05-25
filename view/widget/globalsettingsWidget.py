class GlobalSettingsView:
    def __init__(self, system, on_back):
        self.system = system
        self.ft = system.ft
        self.on_back = on_back # Função de callback para voltar à tela anterior

    def build(self):
        titulo = self.ft.Text("Configurações Globais", size=36, weight=self.ft.FontWeight.W_300, color=self.ft.Colors.WHITE)

        # Lado Esquerdo (Ícone de Rede brilhante)
        icone_rede = self.ft.Container(
            width=160, height=160, shape=self.ft.BoxShape.CIRCLE,
            gradient=self.ft.LinearGradient(colors=["#0052D4", "#7F00FF"]),
            content=self.ft.Container(
                width=150, height=150, shape=self.ft.BoxShape.CIRCLE, bgcolor="#050011",
                content=self.ft.Icon(self.ft.Icons.ROUTER, size=70, color=self.ft.Colors.GREY_400),
                alignment=self.ft.alignment.center
            ),
            alignment=self.ft.alignment.center
        )

        caixa_info = self.ft.Container(
            content=self.ft.Text("Estas configurações\nserão aplicadas como\npadrão para os robôs.", text_align=self.ft.TextAlign.CENTER, size=12, color=self.ft.Colors.GREY_400),
            padding=20, bgcolor="#151125", border_radius=15, width=180
        )

        col_esquerda = self.ft.Column([icone_rede, self.ft.Container(height=20), caixa_info], horizontal_alignment=self.ft.CrossAxisAlignment.CENTER)

        # Lado Direito (Formulário)
        input_rede = self.ft.TextField(
            label="Nome da Rede Wi-Fi (SSID)", 
            width=350, border=self.ft.InputBorder.UNDERLINE, color=self.ft.Colors.WHITE, bgcolor=self.ft.Colors.TRANSPARENT,
            prefix_icon=self.ft.Icons.WIFI
        )

        input_senha = self.ft.TextField(
            label="Senha da Rede", 
            width=350, border=self.ft.InputBorder.UNDERLINE, color=self.ft.Colors.WHITE, bgcolor=self.ft.Colors.TRANSPARENT,
            password=True, can_reveal_password=True, prefix_icon=self.ft.Icons.LOCK_OUTLINE
        )

        # Seletor de Tema
        texto_tema = self.ft.Text("Tema Básico do App", color=self.ft.Colors.GREY_400, size=14)
        
        def criar_botao_tema(nome, icone, cor_ativa):
            return self.ft.Container(
                content=self.ft.Row([self.ft.Icon(icone, size=18, color=self.ft.Colors.WHITE), self.ft.Text(nome, color=self.ft.Colors.WHITE)]),
                padding=self.ft.padding.symmetric(horizontal=20, vertical=10),
                border_radius=20,
                bgcolor=cor_ativa,
                ink=True,
                on_click=lambda e: print(f"Tema {nome} selecionado!")
            )

        paleta_temas = self.ft.Row([
            criar_botao_tema("Escuro", self.ft.Icons.DARK_MODE, "#2A2A35"), 
            criar_botao_tema("Claro", self.ft.Icons.LIGHT_MODE, self.ft.Colors.TRANSPARENT)
        ], spacing=15)

        col_direita = self.ft.Column(
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
            horizontal_alignment=self.ft.CrossAxisAlignment.START
        )

        # Botões inferiores
        btn_salvar = self.ft.Container(
            content=self.ft.Text("SALVAR", weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            alignment=self.ft.alignment.center, width=150, height=45, border_radius=25, ink=True,
            gradient=self.ft.LinearGradient(colors=["#7F00FF", "#0052D4"]),
            on_click=lambda e: self.on_back() 
        )

        btn_cancelar = self.ft.Container(
            content=self.ft.Text("CANCELAR", weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.GREY_300),
            alignment=self.ft.alignment.center, width=150, height=45, border_radius=25, bgcolor="#2A2A35", ink=True,
            on_click=lambda e: self.on_back() 
        )

        botoes_acao = self.ft.Row([btn_salvar, btn_cancelar], alignment=self.ft.MainAxisAlignment.CENTER, spacing=20)

        return self.ft.Column(
            [
                self.ft.Container(height=60),
                titulo,
                self.ft.Container(height=50),
                self.ft.Row([col_esquerda, self.ft.Container(width=50), col_direita], alignment=self.ft.MainAxisAlignment.CENTER, vertical_alignment=self.ft.CrossAxisAlignment.START),
                self.ft.Container(height=60),
                botoes_acao
            ],
            horizontal_alignment=self.ft.CrossAxisAlignment.CENTER, expand=True
        )