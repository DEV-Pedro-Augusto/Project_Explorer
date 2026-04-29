import flet as ft
import time

class LoginView:
    def __init__(self, system, on_login_success):
        self.system = system
        self.on_login_success = on_login_success

    def render(self):
        self.system.page.clean()
        self.system.page.padding = 0 # Remove margens da janela inteira
        
        # --- FUNÇÕES SECUNDÁRIAS ---
        def fechar_popup(dlg):
            dlg.open = False
            self.system.page.update()

        def forgot_password_click(e):
            dlg = ft.AlertDialog(
                title=self.system.ft.Text("Recuperar Senha", weight=self.system.ft.FontWeight.BOLD),
                content=self.system.ft.Text("As instruções de recuperação serão enviadas para o seu e-mail cadastrado."),
                actions=[
                    self.system.ft.TextButton("Entendi", on_click=lambda e: fechar_popup(dlg))
                ],
                shape=self.system.ft.RoundedRectangleBorder(radius=15),
            )
            self.system.page.dialog = dlg
            dlg.open = True
            self.system.page.update()

        def register_click(e):
            print("Redirecionando para a tela de Cadastro...")
            # self.on_register_click()  <-- Descomente para mudar de tela

        # --- CONSTRUÇÃO DA UI (LADO ESQUERDO) ---

        titulo = self.system.ft.Text("Faça seu login.", size=40, weight=self.system.ft.FontWeight.W_900, color=self.system.ft.Colors.WHITE)
        
        # Campos de Entrada 
        input_user = self.system.ft.TextField(
            label="E-mail", 
            width=350, 
            prefix_icon=self.system.ft.Icons.MAIL_OUTLINE,
            border_radius=8,
            border_color=self.system.ft.Colors.TRANSPARENT,
            filled=True,
            bgcolor="#15171E", # Cinza/Azul muito escuro
            color=self.system.ft.Colors.WHITE
        )

        
        input_senha = self.system.ft.TextField(
            label="Senha", 
            width=350, 
            password=True, 
            can_reveal_password=True, 
            prefix_icon=self.system.ft.Icons.LOCK_OUTLINE,
            border_radius=8,
            border_color=self.system.ft.Colors.TRANSPARENT,
            filled=True,
            bgcolor="#15171E",
            color=self.system.ft.Colors.WHITE
        )
        
        # Link "Esqueci minha senha" alinhado à direita
        link_senha = self.system.ft.Container(
            content=self.system.ft.TextButton("Esqueci minha senha", on_click=forgot_password_click, style=self.system.ft.ButtonStyle(color=self.system.ft.Colors.GREY_500)),
            width=350,
            alignment=self.system.ft.alignment.center_right
        )

        # Botão Principal com Gradiente Azul
        btn_login = self.system.ft.Container(
            content=self.system.ft.Text("Entrar", size=16, weight=self.system.ft.FontWeight.BOLD, color=self.system.ft.Colors.WHITE),
            alignment=self.system.ft.alignment.center,
            width=350,
            height=50,
            border_radius=25, # Botão mais arredondado
            ink=True, # Efeito de clique
            on_click=lambda e: self.on_login_success(),
            gradient=self.system.ft.LinearGradient(
                begin=self.system.ft.alignment.center_left,
                end=self.system.ft.alignment.center_right,
                colors=["#0052D4", "#4364F7", "#6FB1FC"] # Gradiente Azul vibrante
            ),
            shadow=self.system.ft.BoxShadow(spread_radius=1, blur_radius=15, color="#0052D4", offset=self.system.ft.Offset(0, 5))
        )

        # Link de Cadastro
        link_cadastro = self.system.ft.Container(
            content=self.system.ft.TextButton("Ainda não tenho uma conta", on_click=register_click, style=self.system.ft.ButtonStyle(color=self.system.ft.Colors.GREY_500)),
            margin=self.system.ft.margin.only(top=20)
        )

        # Agrupando o formulário
        form_column = self.system.ft.Column(
            [
                titulo, 
                self.system.ft.Container(height=40), # Espaçador
                input_user, 
                self.system.ft.Container(height=10), # Espaçador
                input_senha, 
                link_senha,
                self.system.ft.Container(height=20), # Espaçador
                btn_login,
                link_cadastro
            ],
            alignment=self.system.ft.MainAxisAlignment.CENTER,
            horizontal_alignment=self.system.ft.CrossAxisAlignment.START, # Alinhado à esquerda como na sua foto
        )

        # Painel Esquerdo (Preto)
        left_panel = self.system.ft.Container(
            content=form_column,
            width=500, # Largura fixa para o menu lateral
            padding=self.system.ft.padding.only(left=80, right=40),
            bgcolor="#0A0B10", # Preto profundo
            alignment=self.system.ft.alignment.center,
            
            # Animação de entrada
            opacity=0, 
            offset=self.system.ft.Offset(-0.2, 0), # Vem da esquerda
            animate_opacity=700, 
            animate_offset=self.system.ft.Animation(700, self.system.ft.AnimationCurve.EASE_OUT_EXPO)
        )

        # --- CONSTRUÇÃO DA UI (LADO DIREITO - IMAGEM) ---
        # Troque o 'src' abaixo pelo caminho da sua imagem local se preferir
      # --- CONSTRUÇÃO DA UI (LADO DIREITO - IMAGEM) ---
        right_panel = self.system.ft.Container(
            expand=True, # Preenche o resto da tela
            image=self.system.ft.DecorationImage(
                src="assets/carrinho_ft_01.jpg",
                fit=self.system.ft.ImageFit.COVER
            )
        )

        # Layout Principal dividido em Colunas
        layout = self.system.ft.Row(
            controls=[left_panel, right_panel],
            expand=True,
            spacing=0 # Sem espaço entre os painéis
        )
        
        self.system.page.add(layout)
        
        # --- DISPARO DA ANIMAÇÃO ---
        time.sleep(0.1) 
        left_panel.opacity = 1
        left_panel.offset = self.system.ft.Offset(0, 0)
        left_panel.update()