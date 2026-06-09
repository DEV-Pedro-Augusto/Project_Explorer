class CadastroView:
    def __init__(self, system):
        self.system = system
        self.on_back_to_login = self.system.view.page.login
        self.ft = self.system.ft

    def render(self):
        self.system.page.clean()
        self.system.page.padding = 0
        
        # --- FUNÇÕES SECUNDÁRIAS ---
        def fechar_popup(dlg):
            dlg.open = False
            self.system.page.update()
        
        def login_click(e):
            self.system.view.animate.animacaoPagina.animar_tela(self.system, self.on_back_to_login)

        def handle_register(e):
            """Valida os dados e registra o novo usuário."""
            nome = input_nome.value
            email = input_email.value
            telefone = input_telefone.value
            senha = input_senha.value
            confirma_senha = input_confirma_senha.value
            
            print(f"\n📝 DEBUG - Tentando cadastrar: {nome}, {email}, {telefone}")
            
            # Validação básica
            if not nome or not email or not telefone or not senha or not confirma_senha:
                print(f"❌ Campos vazios detectados!")
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
            
            # Valida se as senhas coincidem
            if senha != confirma_senha:
                print(f"❌ Senhas não coincidem!")
                dlg = self.ft.AlertDialog(
                    title=self.ft.Text("Atenção", weight=self.ft.FontWeight.BOLD),
                    content=self.ft.Text("As senhas não coincidem. Verifique e tente novamente."),
                    actions=[
                        self.ft.TextButton("OK", on_click=lambda e: fechar_popup(dlg))
                    ],
                    shape=self.ft.RoundedRectangleBorder(radius=15),
                )
                self.system.page.dialog = dlg
                dlg.open = True
                self.system.page.update()
                return
            
            # Valida o comprimento da senha (mínimo 6 caracteres)
            if len(senha) < 6:
                print(f"❌ Senha muito curta!")
                dlg = self.ft.AlertDialog(
                    title=self.ft.Text("Atenção", weight=self.ft.FontWeight.BOLD),
                    content=self.ft.Text("A senha deve ter no mínimo 6 caracteres."),
                    actions=[
                        self.ft.TextButton("OK", on_click=lambda e: fechar_popup(dlg))
                    ],
                    shape=self.ft.RoundedRectangleBorder(radius=15),
                )
                self.system.page.dialog = dlg
                dlg.open = True
                self.system.page.update()
                return
            
            print(f"✅ Validações passaram, tentando registrar no banco...")
            
            # Tenta registrar o usuário no banco de dados
            usuario = self.system.model.database.registrar_usuario(nome, email, telefone, senha)
            
            print(f"📊 Resultado do registro: {usuario}")
            print(f"🔍 Tipo do resultado: {type(usuario)}")
            
            if usuario and usuario is not None:
                print(f"🎉 Cadastro bem-sucedido! Redirecionando para login...")
                # Mostra popup de sucesso e redireciona automaticamente
                dlg_sucesso = self.ft.AlertDialog(
                    title=self.ft.Text("Cadastro Realizado!", weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.GREEN_400),
                    content=self.ft.Text("Usuário cadastrado com sucesso! Você será redirecionado para o login."),
                    actions=[
                        self.ft.TextButton("Voltar ao Login", on_click=lambda e: (fechar_popup(dlg_sucesso), login_click(e)))
                    ],
                    shape=self.ft.RoundedRectangleBorder(radius=15),
                )
                self.system.page.dialog = dlg_sucesso
                dlg_sucesso.open = True
                self.system.page.update()
                
                # Redireciona automaticamente após 2 segundos
                def redirecionar_automatico():
                    self.system.time.sleep(2)
                    fechar_popup(dlg_sucesso)
                    self.system.time.sleep(0.3)
                    login_click(None)
                
                import threading
                thread = threading.Thread(target=redirecionar_automatico, daemon=True)
                thread.start()
            else:
                # Mostra popup de erro
                print(f"❌ Cadastro falhou!")
                dlg_erro = self.ft.AlertDialog(
                    title=self.ft.Text("Erro no Cadastro", weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.RED_400),
                    content=self.ft.Text("Não foi possível cadastrar o usuário. Verifique se o email já não está cadastrado e tente novamente."),
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
        input_telefone = self.ft.TextField(hint_text="Telefone", prefix_icon=self.ft.Icons.PHONE, **estilo_input)
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

        # LARGURA (420) E ALTURA (680) FIXAS NO CARTÃO!
        glass_card = self.ft.Container(
            content=self.ft.Column(
                [
                    icone_topo, titulo, subtitulo, 
                    self.ft.Container(height=15), 
                    input_nome, input_email, input_telefone, input_senha, input_confirma_senha, 
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
            height=680, 
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