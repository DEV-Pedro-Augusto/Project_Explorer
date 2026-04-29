import flet as ft
import time

class LoginView:
    def __init__(self, page: ft.Page, on_login_success):
        self.page = page
        self.on_login_success = on_login_success

    def render(self):
        self.page.clean()
        self.page.padding = 0 # Remove margens da janela inteira
        
        # --- FUNÇÕES SECUNDÁRIAS ---
        def fechar_popup(dlg):
            dlg.open = False
            self.page.update()

        def forgot_password_click(e):
            dlg = ft.AlertDialog(
                title=ft.Text("Recuperar Senha", weight=ft.FontWeight.BOLD),
                content=ft.Text("As instruções de recuperação serão enviadas para o seu e-mail cadastrado."),
                actions=[
                    ft.TextButton("Entendi", on_click=lambda e: fechar_popup(dlg))
                ],
                shape=ft.RoundedRectangleBorder(radius=15),
            )
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()

        def register_click(e):
            print("Redirecionando para a tela de Cadastro...")
            # self.on_register_click()  <-- Descomente para mudar de tela

        # --- CONSTRUÇÃO DA UI (LADO ESQUERDO) ---

        titulo = ft.Text("Faça seu login.", size=40, weight=ft.FontWeight.W_900, color=ft.Colors.WHITE)
        
        # Campos de Entrada 
        input_user = ft.TextField(
            label="E-mail", 
            width=350, 
            prefix_icon=ft.Icons.MAIL_OUTLINE,
            border_radius=8,
            border_color=ft.Colors.TRANSPARENT,
            filled=True,
            bgcolor="#15171E", # Cinza/Azul muito escuro
            color=ft.Colors.WHITE
        )

        
        input_senha = ft.TextField(
            label="Senha", 
            width=350, 
            password=True, 
            can_reveal_password=True, 
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            border_radius=8,
            border_color=ft.Colors.TRANSPARENT,
            filled=True,
            bgcolor="#15171E",
            color=ft.Colors.WHITE
        )
        
        # Link "Esqueci minha senha" alinhado à direita
        link_senha = ft.Container(
            content=ft.TextButton("Esqueci minha senha", on_click=forgot_password_click, style=ft.ButtonStyle(color=ft.Colors.GREY_500)),
            width=350,
            alignment=ft.alignment.center_right
        )

        # Botão Principal com Gradiente Azul
        btn_login = ft.Container(
            content=ft.Text("Entrar", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            alignment=ft.alignment.center,
            width=350,
            height=50,
            border_radius=25, # Botão mais arredondado
            ink=True, # Efeito de clique
            on_click=lambda e: self.on_login_success(),
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=["#0052D4", "#4364F7", "#6FB1FC"] # Gradiente Azul vibrante
            ),
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color="#0052D4", offset=ft.Offset(0, 5))
        )

        # Link de Cadastro
        link_cadastro = ft.Container(
            content=ft.TextButton("Ainda não tenho uma conta", on_click=register_click, style=ft.ButtonStyle(color=ft.Colors.GREY_500)),
            margin=ft.margin.only(top=20)
        )

        # Agrupando o formulário
        form_column = ft.Column(
            [
                titulo, 
                ft.Container(height=40), # Espaçador
                input_user, 
                ft.Container(height=10), # Espaçador
                input_senha, 
                link_senha,
                ft.Container(height=20), # Espaçador
                btn_login,
                link_cadastro
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START, # Alinhado à esquerda como na sua foto
        )

        # Painel Esquerdo (Preto)
        left_panel = ft.Container(
            content=form_column,
            width=500, # Largura fixa para o menu lateral
            padding=ft.padding.only(left=80, right=40),
            bgcolor="#0A0B10", # Preto profundo
            alignment=ft.alignment.center,
            
            # Animação de entrada
            opacity=0, 
            offset=ft.Offset(-0.2, 0), # Vem da esquerda
            animate_opacity=700, 
            animate_offset=ft.Animation(700, ft.AnimationCurve.EASE_OUT_EXPO)
        )

        # --- CONSTRUÇÃO DA UI (LADO DIREITO - IMAGEM) ---
        # Troque o 'src' abaixo pelo caminho da sua imagem local se preferir
      # --- CONSTRUÇÃO DA UI (LADO DIREITO - IMAGEM) ---
        right_panel = ft.Container(
            expand=True, # Preenche o resto da tela
            image=ft.DecorationImage(
                src="assets/carrinho_ft_01.jpg",
                fit=ft.ImageFit.COVER
            )
        )

        # Layout Principal dividido em Colunas
        layout = ft.Row(
            controls=[left_panel, right_panel],
            expand=True,
            spacing=0 # Sem espaço entre os painéis
        )
        
        self.page.add(layout)
        
        # --- DISPARO DA ANIMAÇÃO ---
        time.sleep(0.1) 
        left_panel.opacity = 1
        left_panel.offset = ft.Offset(0, 0)
        left_panel.update()