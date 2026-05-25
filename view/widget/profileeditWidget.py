class ProfileEditView:
    def __init__(self, system, nome_atual, cor_atual, on_back):
        self.system = system
        self.ft = system.ft
        self.nome_atual = nome_atual
        self.cor_atual = cor_atual
        self.on_back = on_back # Função de callback para voltar à tela anterior

    def build(self):
        titulo = self.ft.Text("Criar perfil" if self.nome_atual == "Novo Perfil" else "Editar perfil", size=36, weight=self.ft.FontWeight.W_300, color=self.ft.Colors.WHITE)

        # Lado Esquerdo (Avatar)
        avatar_preview = self.ft.Container(
            width=160, height=160, shape=self.ft.BoxShape.CIRCLE,
            gradient=self.ft.LinearGradient(colors=self.cor_atual),
            content=self.ft.Container(
                width=150, height=150, shape=self.ft.BoxShape.CIRCLE, bgcolor="#050011",
                content=self.ft.Icon(self.ft.Icons.PERSON_OUTLINE, size=80, color=self.ft.Colors.GREY_400),
                alignment=self.ft.alignment.center
            ),
            alignment=self.ft.alignment.center
        )

        caixa_foto = self.ft.Container(
            content=self.ft.Text("Use o aplicativo para\ncarregar uma foto ou\nescolher um avatar.", text_align=self.ft.TextAlign.CENTER, size=12, color=self.ft.Colors.GREY_400),
            padding=20, bgcolor="#151125", border_radius=15, width=180
        )

        col_esquerda = self.ft.Column([avatar_preview, self.ft.Container(height=20), caixa_foto], horizontal_alignment=self.ft.CrossAxisAlignment.CENTER)

        # Lado Direito (Formulário)
        input_nome = self.ft.TextField(
            label="Nome", value="" if self.nome_atual == "Novo Perfil" else self.nome_atual,
            width=350, border=self.ft.InputBorder.UNDERLINE, color=self.ft.Colors.WHITE, bgcolor=self.ft.Colors.TRANSPARENT
        )

        def criar_bolinha_cor(cores):
            return self.ft.Container(
                width=40, height=40, shape=self.ft.BoxShape.CIRCLE,
                gradient=self.ft.LinearGradient(colors=cores), ink=True,
                on_click=lambda e: print(f"Cor selecionada!") 
            )

        paleta_cores = self.ft.Row([
            criar_bolinha_cor(["#FF007F", "#FF007F"]), 
            criar_bolinha_cor(["#FF007F", "#7F00FF"]), 
            criar_bolinha_cor(["#7F00FF", "#7F00FF"]), 
            criar_bolinha_cor(["#0052D4", "#7F00FF"]), 
            criar_bolinha_cor(["#0052D4", "#6FB1FC"]), 
        ], spacing=15)

        col_direita = self.ft.Column([self.ft.Container(height=40), input_nome, self.ft.Container(height=40), paleta_cores], horizontal_alignment=self.ft.CrossAxisAlignment.START)

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