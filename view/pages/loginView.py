class LoginView:
    def __init__(self, system):
        self.system = system
        self.on_login_success = self.system.view.page.profileSelection
        self.ft = self.system.ft
        

    def render(self):
        self.system.page.clean()
        self.system.page.padding = 0

        # --- FUNÇÕES SECUNDÁRIAS ---
        def fechar_popup(dlg):
            dlg.open = False
            self.system.page.update()

        def forgot_password_click(e):
            dlg = self.ft.AlertDialog(
                title=self.ft.Text("Recuperar Senha", weight=self.ft.FontWeight.BOLD),
                content=self.ft.Text("As instruções serão enviadas para o seu e-mail."),
                actions=[self.ft.TextButton("Entendi", on_click=lambda e: fechar_popup(dlg))],
                shape=self.ft.RoundedRectangleBorder(radius=15),
            )
            self.system.page.dialog = dlg
            dlg.open = True
            self.system.page.update()

        def register_click(e):
            self.system.view.animate.animacaoPagina.animar_tela(self.system, self.system.view.page.cadastro)

        def login_click(e):
            """Valida o login e autentica o usuário."""
            email = input_user.value
            senha = input_senha.value
            
            # Validação básica
            if not email or not senha:
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
            
            # Tenta autenticar no banco de dados 
            usuario = self.system.model.database.autenticar_usuario(email, senha)
            
            if usuario:
                # Armazena o usuário no sistema
                
                self.system.model.usuario_model.definir_usuario(usuario)
                
                # Redireciona para seleção de perfil
                self.system.view.animate.animacaoPagina.animar_tela(self.system, self.on_login_success)
                
            else:
                # Mostra popup de erro de autenticação
                dlg_erro = self.ft.AlertDialog(
                    title=self.ft.Text("Erro de Autenticação", weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.RED_400),
                    content=self.ft.Text("Email ou senha incorretos. Verifique e tente novamente."),
                    actions=[
                        self.ft.TextButton("Tentar Novamente", on_click=lambda e: fechar_popup(dlg_erro))
                    ],
                    shape=self.ft.RoundedRectangleBorder(radius=15),
                )
                self.system.page.dialog = dlg_erro
                dlg_erro.open = True
                self.system.page.update()
            

        # --- CONSTRUÇÃO DO CARTÃO GLASSMORPHISM ---
        
        icone_topo = self.ft.Container(
            content=self.ft.Icon(self.ft.Icons.RADAR, size=35, color=self.ft.Colors.WHITE),
            alignment=self.ft.alignment.center,
            margin=self.ft.margin.only(bottom=5)
        )

        titulo = self.ft.Text("Bem-vindo(a) de volta", size=26, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE, text_align=self.ft.TextAlign.CENTER)
        subtitulo = self.ft.Text("Faça login para continuar", size=13, color=self.ft.Colors.WHITE70, text_align=self.ft.TextAlign.CENTER)

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

        input_user = self.ft.TextField(hint_text="Endereço de E-mail", prefix_icon=self.ft.Icons.PERSON_OUTLINE, **estilo_input)
        input_senha = self.ft.TextField(hint_text="Senha", password=True, can_reveal_password=True, prefix_icon=self.ft.Icons.LOCK_OUTLINE, **estilo_input)
        
        opcoes_extras = self.ft.Row(
            [
                self.ft.Checkbox(label="Lembrar-me", value=False, fill_color=self.ft.Colors.with_opacity(0.2, self.ft.Colors.WHITE), label_style=self.ft.TextStyle(color=self.ft.Colors.WHITE70, size=12)),
                self.ft.TextButton("Esqueceu a senha?", on_click=forgot_password_click, style=self.ft.ButtonStyle(color=self.ft.Colors.WHITE70))
            ],
            alignment=self.ft.MainAxisAlignment.SPACE_BETWEEN,
            width=340
        )

        btn_login = self.ft.Container(
            content=self.ft.Row([self.ft.Text("Entrar", size=15, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE), self.ft.Icon(self.ft.Icons.ARROW_FORWARD, color=self.ft.Colors.WHITE, size=18)], alignment=self.ft.MainAxisAlignment.CENTER),
            alignment=self.ft.alignment.center, width=340, height=45, border_radius=10, ink=True, on_click=login_click,
            bgcolor=self.ft.Colors.with_opacity(0.2, self.ft.Colors.WHITE),
            border=self.ft.border.all(1, self.ft.Colors.with_opacity(0.4, self.ft.Colors.WHITE)),
        )

        rodape = self.ft.Row([
            self.ft.Text("Não tem uma conta?", size=13, color=self.ft.Colors.WHITE70),
            self.ft.TextButton("Criar uma", on_click=register_click, style=self.ft.ButtonStyle(color=self.ft.Colors.CYAN_200))
        ], alignment=self.ft.MainAxisAlignment.CENTER, spacing=0)

        glass_card = self.ft.Container(
            content=self.ft.Column(
                [
                    icone_topo, titulo, subtitulo, 
                    self.ft.Container(height=15), 
                    input_user, input_senha, opcoes_extras, 
                    btn_login, 
                    self.ft.Container(height=15), 
                    rodape
                ],
                horizontal_alignment=self.ft.CrossAxisAlignment.CENTER, 
                alignment=self.ft.MainAxisAlignment.CENTER, 
                spacing=8
            ),
            width=420, 
            height=550, 
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