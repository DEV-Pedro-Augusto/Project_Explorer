import flet as ft
from view.pages.inventoryView import InventoryView
from view.pages.sidebar import Sidebar

class DashboardView:
    def __init__(self, page: ft.Page, nome_carrinho, db_client=None):
        self.page = page
        self.nome_carrinho = nome_carrinho
        self.db_client = db_client
        self.current_view = 0  # Rastreia a view atual

    def mostrar_popup_pareamento(self):
        dlg = ft.AlertDialog(
            title=ft.Text("Pareamento Necessário", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            content=ft.Text(f"Use este código no {self.nome_carrinho} para sincronizar:\n\n[ OI ]", size=18, text_align=ft.TextAlign.CENTER),
            actions=[
                ft.ElevatedButton("Entendi e Conectei", on_click=lambda e: self.fechar_popup(dlg), bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE)
            ],
            bgcolor="#121826", # Cor escura para combinar
            shape=ft.RoundedRectangleBorder(radius=10)
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def fechar_popup(self, dlg):
        dlg.open = False
        self.page.update()

    def handle_navigation(self, index):
        """Gerencia a navegação entre as diferentes seções do dashboard."""
        self.current_view = index
        if index == 0:
            # Home/Dashboard
            self.render()
        elif index == 1:
            # Notificações
            self.page.clean()
            self.page.add(ft.Text("Notificações (Em construção)", color=ft.Colors.WHITE, size=24))
        elif index == 2:
            # Status/Velocidade
            self.page.clean()
            self.page.add(ft.Text("Status do Sistema (Em construção)", color=ft.Colors.WHITE, size=24))
        elif index == 3:
            # Calendário
            self.page.clean()
            self.page.add(ft.Text("Calendário (Em construção)", color=ft.Colors.WHITE, size=24))
        elif index == 4:
            # Configurações
            self.page.clean()
            self.page.add(ft.Text("Configurações (Em construção)", color=ft.Colors.WHITE, size=24))
        elif index == 5:
            # Eventos/Prêmios
            self.page.clean()
            self.page.add(ft.Text("Eventos (Em construção)", color=ft.Colors.WHITE, size=24))

    def render(self):
        self.page.clean()
        self.page.bgcolor = "#060A14" # Fundo principal super escuro (Deep Navy)
        self.page.padding = 10
        
        # --- SIDEBAR (Barra Lateral Esquerda) ---
        sidebar = Sidebar(on_navigate=self.handle_navigation)

        # --- FUNÇÕES GERADORAS DE COMPONENTES ---

        # 1. Cartão de Alerta (Canto superior esquerdo)
        alert_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=20),
                    ft.Text("ALERTA DE SEGURANÇA", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=14)
                ]),
                ft.Text(
                    "Detectado: Concentração elevada de Gás (NH3) na área de teste. Valor Atual: 135 ppm (Limite de Segurança: 50 ppm).", 
                    color=ft.Colors.GREY_300, 
                    size=12
                )
            ], spacing=5),
            bgcolor="#0B132B", 
            padding=15,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.RED_900), # Bordinha vermelha sutil
            expand=3 # Ocupa 3 partes do espaço superior
        )

        # 2. Minicartões de Sensores (Topo direita)
        def create_sensor_badge(icon_name, color, value, unit, label):
            return ft.Row([
                ft.Container(
                    content=ft.Icon(icon_name, color=color, size=28),
                    padding=8,
                    border=ft.border.all(1, color),
                    border_radius=10,
                    bgcolor="#0A1122"
                ),
                ft.Column([
                    ft.Row([
                        ft.Text(value, size=22, weight=ft.FontWeight.W_900, color=ft.Colors.WHITE), 
                        ft.Text(unit, size=12, color=ft.Colors.GREY_400)
                    ], spacing=2),
                    ft.Text(label, size=12, color=ft.Colors.GREY_500)
                ], spacing=0)
            ], spacing=10)

        sensors_row = ft.Container(
            content=ft.Row([
                create_sensor_badge(ft.Icons.WATER_DROP, ft.Colors.CYAN_400, "58", "%", "Umidade"),
                create_sensor_badge(ft.Icons.WB_SUNNY, ft.Colors.YELLOW_400, "320", "lux", "Luminosidade"),
                create_sensor_badge(ft.Icons.STRAIGHTEN, ft.Colors.BLUE_300, "87", "cm", "Distância"),
                create_sensor_badge(ft.Icons.AIR, ft.Colors.GREEN_400, "135", "ppm", "Gás"),
                create_sensor_badge(ft.Icons.THERMOSTAT, ft.Colors.RED_500, "27.1", "°C", "Temperatura"),
                create_sensor_badge(ft.Icons.SPEED, ft.Colors.PURPLE_400, "1013", "hPa", "Pressão"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            expand=7 # Ocupa 7 partes do espaço superior
        )

        top_section = ft.Row([alert_card, sensors_row], spacing=20)

        inventory_button = ft.Container(
            content=ft.ElevatedButton(
                "Ver inventário completo",
                on_click=lambda e: InventoryView(self.page, self.db_client, on_back=self.render).render(),
                bgcolor="#2563EB",
                color=ft.Colors.WHITE,
                width=220,
                height=48
            ),
            alignment=ft.alignment.center_left,
            padding=ft.padding.symmetric(vertical=10)
        )

        # 3. Cartões de Status (A linha do meio)
        def create_info_card(title, value, icon_name=None, highlight=False):
            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(icon_name, size=16, color=ft.Colors.GREY_400) if icon_name else ft.Container(),
                        ft.Text(title, color=ft.Colors.GREY_400, size=13)
                    ]),
                    ft.Text(value, color=ft.Colors.WHITE, size=20, weight=ft.FontWeight.BOLD)
                ], spacing=10),
                bgcolor="#0B1A40" if highlight else "#111827", # Um fica mais azul igual na imagem
                padding=20,
                border_radius=10,
                expand=1
            )

        status_row = ft.Row([
            create_info_card("Estabilidade Atmosférica", "Pressão ambiente dentro da faixa normal.", ft.Icons.SMART_TOY),
            create_info_card("Status do Robô", "Online - Bateria: 82%", ft.Icons.TRENDING_UP, highlight=True),
            create_info_card("Leituras Coletadas", "112", ft.Icons.PERSON_OUTLINE),
            create_info_card("Última Atualização", "29 min", ft.Icons.FACT_CHECK_OUTLINED),
        ], spacing=20)

        # 4. Área de Gráficos (Mockups estilizados)
        def create_mock_chart(title, subtitle, icon, color):
            # Cria um painel bonito simulando o espaço do gráfico
            return ft.Container(
                content=ft.Column([
                    ft.Text(title, color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.W_500),
                    ft.Container(expand=True), # Empurra o ícone pro meio
                    ft.Icon(icon, size=60, color=color, opacity=0.3),
                    ft.Text(subtitle, color=ft.Colors.GREY_500, size=12),
                    ft.Container(expand=True),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor="#111827",
                padding=20,
                border_radius=10,
                expand=1,
                border=ft.border.all(1, "#1E293B")
            )

        charts_row_1 = ft.Row([
            create_mock_chart("Sensor Data Distribution", "Gráfico de Pizza em breve", ft.Icons.PIE_CHART, ft.Colors.BLUE_400),
            create_mock_chart("Temperature per Hour", "Gráfico de Linha em breve", ft.Icons.SHOW_CHART, ft.Colors.CYAN_400),
            create_mock_chart("Distance traveled in seven days", "Gráfico de Barras em breve", ft.Icons.BAR_CHART, ft.Colors.BLUE_600),
        ], expand=True, spacing=20)

        charts_row_2 = ft.Row([
            create_mock_chart("Air Quality Status", "Métrica Detalhada", ft.Icons.AIR, ft.Colors.RED_400),
            create_mock_chart("Ammonia (NH3) Concentration", "Histórico de 24h", ft.Icons.SCATTER_PLOT, ft.Colors.PURPLE_400),
            create_mock_chart("Alcohol Variation", "Níveis de variação", ft.Icons.STACKED_BAR_CHART, ft.Colors.YELLOW_400),
        ], expand=True, spacing=20)


        # --- MONTAGEM DO LAYOUT FINAL ---
        area_dashboard = ft.Column([
            top_section,
            inventory_button,
            ft.Container(height=10),
            status_row,
            ft.Container(height=10),
            charts_row_1,
            charts_row_2
        ], expand=True, scroll=ft.ScrollMode.AUTO) # Scroll caso a tela seja pequena

        layout_principal = ft.Row([
            sidebar, 
            ft.VerticalDivider(width=1, color="#1A2235"), 
            area_dashboard
        ], expand=True)
        
        self.page.add(layout_principal)
        self.page.update()
        
        # Dispara o popup logo após desenhar a tela (apenas na primeira renderização)
        if self.current_view == 0:
            self.mostrar_popup_pareamento()