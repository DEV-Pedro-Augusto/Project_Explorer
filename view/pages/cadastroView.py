class CadastroView:
    def __init__(self, system):
        self.system = system
        self.on_back_to_login = self.system.view.page.login
        self.ft = self.system.ft

    def render(self):
        self.system.page.clean()
        self.system.page.padding = 0
        
        def login_click(e):
            self.system.view.animate.animacaoPagina.animar_tela(self.system, self.on_back_to_login)

        def handle_register(e):
            # Lógica de cadastro virá aqui no futuro
            login_click(e) 

        # --- CONSTRUÇÃO DO CARTÃO GLASSMORPHISM ---
        
        icone_topo = self.ft.Container(
            content=self.ft.Icon(self.ft.Icons.PERSON_ADD_ALT_1, size=35, color=self.ft.Colors.WHITE),
            alignment=self.ft.alignment.center,
            margin=self.ft.margin.only(bottom=5)
        )

        titulo = self.ft.Text("Criar Conta", size=26, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE, text_align=self.ft.TextAlign.CENTER)
        subtitulo = self.ft.Text("Junte-se a nós para começar sua jornada", size=13, color=self.ft.Colors.WHITE70, text_align=self.ft.TextAlign.CENTER)

        estilo_input = {
            "width": 340,
            "bgcolor": self.ft.Colors.with_opacity(0.1, self.ft.Colors.WHITE),
            "border_color": self.ft.Colors.with_opacity(0.3, self.ft.Colors.WHITE),
            "color": self.ft.Colors.WHITE,
            "border_radius": 10,
            "cursor_color": self.ft.Colors.WHITE,
            "content_padding": 15,
            "text_size": 14
        }

        input_nome = self.ft.TextField(hint_text="Nome Completo", prefix_icon=self.ft.Icons.BADGE, **estilo_input)
        input_email = self.ft.TextField(hint_text="Endereço de E-mail", prefix_icon=self.ft.Icons.MAIL_OUTLINE, **estilo_input)
        input_senha = self.ft.TextField(hint_text="Senha", password=True, can_reveal_password=True, prefix_icon=self.ft.Icons.LOCK_OUTLINE, **estilo_input)
        input_confirma_senha = self.ft.TextField(hint_text="Confirmar Senha", password=True, can_reveal_password=True, prefix_icon=self.ft.Icons.LOCK_RESET_OUTLINED, **estilo_input)

        btn_register = self.ft.Container(
            content=self.ft.Row([self.ft.Text("Cadastrar", size=15, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE), self.ft.Icon(self.ft.Icons.ARROW_FORWARD, color=self.ft.Colors.WHITE, size=18)], alignment=self.ft.MainAxisAlignment.CENTER),
            alignment=self.ft.alignment.center, width=340, height=45, border_radius=10, ink=True, on_click=handle_register,
            bgcolor=self.ft.Colors.with_opacity(0.2, self.ft.Colors.WHITE),
            border=self.ft.border.all(1, self.ft.Colors.with_opacity(0.4, self.ft.Colors.WHITE)),
        )

        rodape = self.ft.Row([
            self.ft.Text("Já tem uma conta?", size=13, color=self.ft.Colors.WHITE70),
            self.ft.TextButton("Entrar", on_click=login_click, style=self.ft.ButtonStyle(color=self.ft.Colors.CYAN_200))
        ], alignment=self.ft.MainAxisAlignment.CENTER, spacing=0)

        # LARGURA (420) E ALTURA (600) FIXAS NO CARTÃO!
        glass_card = self.ft.Container(
            content=self.ft.Column(
                [
                    icone_topo, titulo, subtitulo, 
                    self.ft.Container(height=15), 
                    input_nome, input_email, input_senha, input_confirma_senha, 
                    self.ft.Container(height=10), 
                    btn_register, 
                    self.ft.Container(height=5), 
                    rodape
                ],
                horizontal_alignment=self.ft.CrossAxisAlignment.CENTER, 
                alignment=self.ft.MainAxisAlignment.CENTER, 
                spacing=8
            ),
            width=420, 
            height=600, 
            padding=30, 
            border_radius=20,
            bgcolor=self.ft.Colors.with_opacity(0.05, self.ft.Colors.WHITE),
            border=self.ft.border.all(1.5, self.ft.Colors.with_opacity(0.2, self.ft.Colors.WHITE)),
            blur=15, 
            alignment=self.ft.alignment.center,
            shadow=self.ft.BoxShadow(blur_radius=50, color=self.ft.Colors.with_opacity(0.1, self.ft.Colors.BLACK))
        )

        layout = self.ft.Container(
            expand=True,
            image=self.ft.DecorationImage(src="assets/bg_aurora.png", fit=self.ft.ImageFit.COVER),
            alignment=self.ft.alignment.center,
            content=glass_card,
            opacity=0, 
            animate_opacity=800
        )
        
        self.system.page.add(layout)
        self.system.time.sleep(0.1) 
        layout.opacity = 1
        layout.update()