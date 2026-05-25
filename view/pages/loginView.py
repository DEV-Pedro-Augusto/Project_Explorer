
import time

class LoginView:
    def __init__(self, system):
        self.system = system
        self.on_login_success = self.system.view.page.profileSelection
        self.ft = self.system.ft

    def render(self):
        self.system.page.clean()
        self.system.page.padding = 0 # Remove margens da janela inteira
        
        # --- FUNÇÕES SECUNDÁRIAS ---
        def fechar_popup(dlg):
            dlg.open = False
            self.system.page.update()

        def forgot_password_click(e):
            dlg = self.ft.AlertDialog(
                title=self.ft.Text("Recuperar Senha", weight=self.ft.FontWeight.BOLD),
                content=self.ft.Text("As instruções de recuperação serão enviadas para o seu e-mail cadastrado."),
                actions=[
                    self.ft.TextButton("Entendi", on_click=lambda e: fechar_popup(dlg))
                ],
                shape=self.ft.RoundedRectangleBorder(radius=15),
            )
            self.system.page.dialog = dlg
            dlg.open = True
            self.system.page.update()

        def register_click(e):
           self.system.view.page.cadastro(self.system).render()

        def handle_login(e):
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
                self.system.definir_usuario(usuario)
                # Redireciona para seleção de perfil
                self.on_login_success(self.system).render()
            else:
                # Mostra erro de autenticação
                dlg = self.ft.AlertDialog(
                    title=self.ft.Text("Login Inválido", weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.RED_400),
                    content=self.ft.Text("E-mail ou senha incorretos. Tente novamente."),
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

        titulo = self.ft.Text("Faça seu login.", size=40, weight=self.ft.FontWeight.W_900, color=self.ft.Colors.WHITE)
        
        # Campos de Entrada 
        input_user = self.ft.TextField(
            label="E-mail", 
            width=350, 
            prefix_icon=self.ft.Icons.MAIL_OUTLINE,
            border_radius=8,
            border_color=self.ft.Colors.TRANSPARENT,
            filled=True,
            bgcolor="#15171E", # Cinza/Azul muito escuro
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
        
        # Link "Esqueci minha senha" alinhado à direita
        link_senha = self.ft.Container(
            content=self.ft.TextButton("Esqueci minha senha", on_click=forgot_password_click, style=self.ft.ButtonStyle(color=self.ft.Colors.GREY_500)),
            width=350,
            alignment=self.ft.alignment.center_right
        )

        # Botão Principal com Gradiente Azul
        btn_login = self.ft.Container(
            content=self.ft.Text("Entrar", size=16, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            alignment=self.ft.alignment.center,
            width=350,
            height=50,
            border_radius=25, # Botão mais arredondado
            ink=True, # Efeito de clique
            on_click=handle_login,
            gradient=self.ft.LinearGradient(
                begin=self.ft.alignment.center_left,
                end=self.ft.alignment.center_right,
                colors=["#0052D4", "#4364F7", "#6FB1FC"] # Gradiente Azul vibrante
            ),
            shadow=self.ft.BoxShadow(spread_radius=1, blur_radius=15, color="#0052D4", offset=self.ft.Offset(0, 5))
        )

        # Link de Cadastro
        link_cadastro = self.ft.Container(
            content=self.ft.TextButton("Ainda não tenho uma conta", on_click=register_click, style=self.ft.ButtonStyle(color=self.ft.Colors.GREY_500)),
            margin=self.ft.margin.only(top=20)
        )

        # Agrupando o formulário
        form_column = self.ft.Column(
            [
                titulo, 
                self.ft.Container(height=40), # Espaçador
                input_user, 
                self.ft.Container(height=10), # Espaçador
                input_senha, 
                link_senha,
                self.ft.Container(height=20), # Espaçador
                btn_login,
                link_cadastro
            ],
            alignment=self.ft.MainAxisAlignment.CENTER,
            horizontal_alignment=self.ft.CrossAxisAlignment.START, # Alinhado à esquerda como na sua foto
        )

        # Painel Esquerdo (Preto)
        left_panel = self.ft.Container(
            content=form_column,
            width=500, # Largura fixa para o menu lateral
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
        # Troque o 'src' abaixo pelo caminho da sua imagem local se preferir
      # --- CONSTRUÇÃO DA UI (LADO DIREITO - IMAGEM) ---
        right_panel = self.ft.Container(
            expand=True, # Preenche o resto da tela
            image=self.ft.DecorationImage(
                src="assets/carrinho_ft_01.jpg",
                fit=self.ft.ImageFit.COVER
            )
        )

        # Layout Principal dividido em Colunas
        layout = self.ft.Row(
            controls=[left_panel, right_panel],
            expand=True,
            spacing=0 # Sem espaço entre os painéis
        )
        
        self.system.page.add(layout)
        
        # --- DISPARO DA ANIMAÇÃO ---
        time.sleep(0.1) 
        left_panel.opacity = 1
        left_panel.offset = self.ft.Offset(0, 0)
        left_panel.update()