

class CadastroView:
    def __init__(self, system):
        self.system = system
        # Definimos para onde ele vai após o cadastro (pode ir para o login ou direto para a seleção de perfil)
        self.on_register_success = self.system.view.page.login # Após cadastrar, volta pro login
        self.on_back_to_login = self.system.view.page.login
        self.ft = self.system.ft

    def render(self):
        self.system.page.clean()
        self.system.page.padding = 0 # Remove margens da janela inteira
        
        # --- FUNÇÕES SECUNDÁRIAS ---
        def fechar_popup(dlg):
            dlg.open = False
            self.system.page.update()

        def login_click(e):
            
            # Renderiza a tela de login
            self.on_back_to_login(self.system).render()

        def handle_register(e):
            # Aqui entraria a lógica de validação de senha, salvar no banco, etc.
         
            
            # Simulando sucesso e voltando para o login
            dlg = self.ft.AlertDialog(
                title=self.ft.Text("Cadastro Realizado", weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.GREEN_400),
                content=self.ft.Text("Sua conta foi criada com sucesso! Faça o login para continuar."),
                actions=[
                    self.ft.TextButton("Ir para Login", on_click=lambda e: (fechar_popup(dlg), self.on_register_success(self.system).render()))
                ],
                shape=self.ft.RoundedRectangleBorder(radius=15),
                bgcolor="#15171E"
            )
            self.system.page.dialog = dlg
            dlg.open = True
            self.system.page.update()


        # --- CONSTRUÇÃO DA UI (LADO ESQUERDO) ---

        titulo = self.ft.Text("Crie sua conta.", size=40, weight=self.ft.FontWeight.W_900, color=self.ft.Colors.WHITE)
        subtitulo = self.ft.Text("Preencha os dados abaixo para se registrar.", size=14, color=self.ft.Colors.GREY_500)
        
        # Campos de Entrada 
        input_nome = self.ft.TextField(
            label="Nome Completo", 
            width=350, 
            prefix_icon=self.ft.Icons.PERSON_OUTLINE,
            border_radius=8,
            border_color=self.ft.Colors.TRANSPARENT,
            filled=True,
            bgcolor="#15171E", # Cinza/Azul muito escuro
            color=self.ft.Colors.WHITE
        )

        input_email = self.ft.TextField(
            label="E-mail", 
            width=350, 
            prefix_icon=self.ft.Icons.MAIL_OUTLINE,
            border_radius=8,
            border_color=self.ft.Colors.TRANSPARENT,
            filled=True,
            bgcolor="#15171E", 
            color=self.ft.Colors.WHITE
        )
        
        input_senha = self.ft.TextField(
            label="Senha", 
            width=350, 
            password=True, 
            can_reveal_password=True, 
            prefix_icon=self.ft.Icons.LOCK_OUTLINE,
            border_radius=8,
            border_color=self.ft.Colors.TRANSPARENT,
            filled=True,
            bgcolor="#15171E",
            color=self.ft.Colors.WHITE
        )

        input_confirma_senha = self.ft.TextField(
            label="Confirmar Senha", 
            width=350, 
            password=True, 
            can_reveal_password=True, 
            prefix_icon=self.ft.Icons.LOCK_RESET_OUTLINED,
            border_radius=8,
            border_color=self.ft.Colors.TRANSPARENT,
            filled=True,
            bgcolor="#15171E",
            color=self.ft.Colors.WHITE
        )

        # Botão Principal com Gradiente Verde (Para diferenciar do Azul do Login)
        btn_register = self.ft.Container(
            content=self.ft.Text("Cadastrar", size=16, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            alignment=self.ft.alignment.center,
            width=350,
            height=50,
            border_radius=25, 
            ink=True, 
            on_click=handle_register,
            gradient=self.ft.LinearGradient(
                begin=self.ft.alignment.center_left,
                end=self.ft.alignment.center_right,
                colors=["#00B4DB", "#0083B0"] # Gradiente Cyan/Azul
            ),
            shadow=self.ft.BoxShadow(spread_radius=1, blur_radius=15, color="#0083B0", offset=self.ft.Offset(0, 5)),
            margin=self.ft.margin.only(top=10)
        )

        # Link de Voltar para o Login
        link_login = self.ft.Container(
            content=self.ft.Row([
                self.ft.Text("Já tem uma conta?", color=self.ft.Colors.GREY_500),
                self.ft.TextButton("Faça login aqui", on_click=login_click, style=self.ft.ButtonStyle(color=self.ft.Colors.BLUE_400))
            ], alignment=self.ft.MainAxisAlignment.START),
            margin=self.ft.margin.only(top=20)
        )

        # Agrupando o formulário
        form_column = self.ft.Column(
            [
                titulo, 
                subtitulo,
                self.ft.Container(height=30), # Espaçador
                input_nome,
                self.ft.Container(height=10),
                input_email, 
                self.ft.Container(height=10),
                input_senha, 
                self.ft.Container(height=10),
                input_confirma_senha,
                self.ft.Container(height=20), # Espaçador
                btn_register,
                link_login
            ],
            alignment=self.ft.MainAxisAlignment.CENTER,
            horizontal_alignment=self.ft.CrossAxisAlignment.START, 
        )

        # Painel Esquerdo (Preto)
        left_panel = self.ft.Container(
            content=form_column,
            width=500, # Largura fixa 
            padding=self.ft.padding.only(left=80, right=40),
            bgcolor="#0A0B10", # Preto profundo
            alignment=self.ft.alignment.center,
            
            # Animação de entrada
            opacity=0, 
            offset=self.ft.Offset(-0.2, 0), # Vem da esquerda
            animate_opacity=700, 
            animate_offset=self.ft.Animation(700, self.ft.AnimationCurve.EASE_OUT_EXPO)
        )

        # --- CONSTRUÇÃO DA UI (LADO DIREITO - IMAGEM) ---
        right_panel = self.ft.Container(
            expand=True, # Preenche o resto da tela
            image=self.ft.DecorationImage(
                src="assets/carrinho_ft_01.jpg", # Usando a mesma imagem
                fit=self.ft.ImageFit.COVER
            )
        )

        # Layout Principal dividido em Colunas
        layout = self.ft.Row(
            controls=[left_panel, right_panel],
            expand=True,
            spacing=0 
        )
        
        self.system.page.add(layout)
        
        # --- DISPARO DA ANIMAÇÃO ---
        self.system.time.sleep(0.1) 
        left_panel.opacity = 1
        left_panel.offset = self.ft.Offset(0, 0)
        left_panel.update()