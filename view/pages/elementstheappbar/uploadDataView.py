import flet as ft


class UploadDataView:
    def __init__(self, system):
        self.system = system
        self.page = system.page
        self.ft = system.ft

    def render(self):
        ft = self.ft

        # Tenta carregar sessões e carrinhos do modelo, com fallback
        try:
            sess = []
            if hasattr(self.system.model, 'database') and hasattr(self.system.model.database, 'listar_sessoes'):
                sess = self.system.model.database.listar_sessoes() or []
        except Exception:
            sess = []

        try:
            carrinhos = []
            if hasattr(self.system.model, 'database') and hasattr(self.system.model.database, 'listar_carrinhos_usuario'):
                uid = None
                try:
                    uid = self.system.obter_id_usuario()
                except Exception:
                    uid = None
                carrinhos = self.system.model.database.listar_carrinhos_usuario(uid) or []
        except Exception:
            carrinhos = []

        session_options = [ft.dropdown.Option(str(s)) for s in (sess or ["Sessão 1", "Sessão 2"]) ]
        carrinho_options = [ft.dropdown.Option(str(c.get('nomes_dispositivos', c))) if isinstance(c, dict) else ft.dropdown.Option(str(c)) for c in (carrinhos or ["Carrinho A"]) ]

        session_dropdown = ft.Dropdown(width=300, options=session_options, value=(session_options[0].text if session_options else None))
        carrinho_dropdown = ft.Dropdown(width=300, options=carrinho_options, value=(carrinho_options[0].text if carrinho_options else None))

        leituras_field = ft.TextField(label="Leituras (JSON/CSV)", multiline=True, width=600, height=120)

        def on_submit(e):
            sess_val = session_dropdown.value
            carr_val = carrinho_dropdown.value
            leituras = leituras_field.value
            print(f"Enviar leituras: sess={sess_val}, carrinho={carr_val}, leituras={leituras}")
            # Placeholder: ligar ao serviço de envio real, se disponível
            if hasattr(self.system, 'service') and hasattr(self.system.service, 'enviar_leituras'):
                try:
                    self.system.service.enviar_leituras(sess_val, carr_val, leituras)
                except Exception as ex:
                    print(f"Erro ao enviar: {ex}")
            # Feedback visual
            self.page.snack_bar = ft.SnackBar(ft.Text("Dados enviados (simulação)."))
            self.page.snack_bar.open = True
            self.page.update()

        submit_btn = ft.ElevatedButton(text="Enviar", on_click=on_submit, bgcolor=ft.Colors.BLUE_400)

        content = ft.Column([
            ft.Text("Enviar Leituras", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(height=10),
            ft.Row([ft.Column([ft.Text("Sessão", color=ft.Colors.GREY_300), session_dropdown]), ft.Container(width=20), ft.Column([ft.Text("Carrinho", color=ft.Colors.GREY_300), carrinho_dropdown])], spacing=20),
            ft.Container(height=10),
            leituras_field,
            ft.Container(height=12),
            ft.Row([submit_btn], alignment=ft.MainAxisAlignment.END)
        ], expand=True)

        # Limpa e adiciona
        self.page.clean()
        self.page.add(ft.Container(content, expand=True, padding=20))
