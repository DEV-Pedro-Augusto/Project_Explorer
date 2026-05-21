import flet as ft

class DashboardView:
    def __init__(self, system, nome_carrinho):
        self.system = system
        self.nome_carrinho = nome_carrinho
        self.ft = self.system.ft

    def mostrar_popup_pareamento(self):
        dlg = self.ft.AlertDialog(
            title=self.ft.Text("Pareamento Necessário", weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            content=self.ft.Text(f"Use este código no {self.nome_carrinho} para sincronizar:\n\n[ OI ]", size=18, text_align=self.ft.TextAlign.CENTER),
            actions=[
                self.ft.ElevatedButton("Entendi e Conectei", on_click=lambda e: self.fechar_popup(dlg), bgcolor=self.ft.Colors.BLUE_600, color=self.ft.Colors.WHITE)
            ],
            bgcolor="#121826", # Cor escura para combinar
            shape=self.ft.RoundedRectangleBorder(radius=10)
        )
        self.system.page.dialog = dlg
        dlg.open = True
        self.system.page.update()

    def fechar_popup(self, dlg):
        dlg.open = False
        self.system.page.update()

    def render(self):
        # --- FUNÇÕES GERADORAS DE COMPONENTES ---

        # 1. Cartão de Alerta (Canto superior esquerdo)
        alert_card = self.ft.Container(
            content=self.ft.Column([
                self.ft.Row([
                    self.ft.Icon(self.ft.Icons.WARNING_AMBER_ROUNDED, color=self.ft.Colors.AMBER, size=20),
                    self.ft.Text("ALERTA DE SEGURANÇA", weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE, size=14)
                ]),
                self.ft.Text(
                    "Detectado: Concentração elevada de Gás (NH3) na área de teste. Valor Atual: 135 ppm (Limite de Segurança: 50 ppm).", 
                    color=self.ft.Colors.GREY_300, 
                    size=12
                )
            ], spacing=5),
            bgcolor="#0B132B", 
            padding=15,
            border_radius=10,
            border=self.ft.border.all(1, self.ft.Colors.RED_900),
            expand=3
        )

        # 2. Minicartões de Sensores (Topo direita)
        def create_sensor_badge(icon_name, color, value, unit, label):
            return self.ft.Row([
                self.ft.Container(
                    content=self.ft.Icon(icon_name, color=color, size=28),
                    padding=8,
                    border=self.ft.border.all(1, color),
                    border_radius=10,
                    bgcolor="#0A1122"
                ),
                self.ft.Column([
                    self.ft.Row([
                        self.ft.Text(value, size=22, weight=self.ft.FontWeight.W_900, color=self.ft.Colors.WHITE), 
                        self.ft.Text(unit, size=12, color=self.ft.Colors.GREY_400)
                    ], spacing=2),
                    self.ft.Text(label, size=12, color=self.ft.Colors.GREY_500)
                ], spacing=0)
            ], spacing=10)

        sensors_row = self.ft.Container(
            content=self.ft.Row([
                create_sensor_badge(self.ft.Icons.WATER_DROP, self.ft.Colors.CYAN_400, "58", "%", "Umidade"),
                create_sensor_badge(self.ft.Icons.WB_SUNNY, self.ft.Colors.YELLOW_400, "320", "lux", "Luminosidade"),
                create_sensor_badge(self.ft.Icons.STRAIGHTEN, self.ft.Colors.BLUE_300, "87", "cm", "Distância"),
                create_sensor_badge(self.ft.Icons.AIR, self.ft.Colors.GREEN_400, "135", "ppm", "Gás"),
                create_sensor_badge(self.ft.Icons.THERMOSTAT, self.ft.Colors.RED_500, "27.1", "°C", "Temperatura"),
                create_sensor_badge(self.ft.Icons.SPEED, self.ft.Colors.PURPLE_400, "1013", "hPa", "Pressão"),
            ], alignment=self.ft.MainAxisAlignment.SPACE_BETWEEN),
            expand=7 
        )

        top_section = self.ft.Row([alert_card, sensors_row], spacing=20)

        # 3. Cartões de Status (A linha do meio)
        def create_info_card(title, value, icon_name=None, highlight=False):
            return self.ft.Container(
                content=self.ft.Column([
                    self.ft.Row([
                        self.ft.Icon(icon_name, size=16, color=self.ft.Colors.GREY_400) if icon_name else self.ft.Container(),
                        self.ft.Text(title, color=self.ft.Colors.GREY_400, size=13)
                    ]),
                    self.ft.Text(value, color=self.ft.Colors.WHITE, size=20, weight=self.ft.FontWeight.BOLD)
                ], spacing=10),
                bgcolor="#0B1A40" if highlight else "#111827",
                padding=20,
                border_radius=10,
                expand=1
            )

        status_row = self.ft.Row([
            create_info_card("Estabilidade Atmosférica", "Pressão ambiente dentro da faixa normal.", self.ft.Icons.SMART_TOY),
            create_info_card("Status do Robô", "Online - Bateria: 82%", self.ft.Icons.TRENDING_UP, highlight=True),
            create_info_card("Leituras Coletadas", "112", self.ft.Icons.PERSON_OUTLINE),
            create_info_card("Última Atualização", "29 min", self.ft.Icons.FACT_CHECK_OUTLINED),
        ], spacing=20)

        # 4. Área de Gráficos (Mockups estilizados)
        def create_mock_chart(title, subtitle, icon, color):
            return self.ft.Container(
                content=self.ft.Column([
                    self.ft.Text(title, color=self.ft.Colors.WHITE, size=14, weight=self.ft.FontWeight.W_500),
                    self.ft.Container(expand=True), 
                    self.ft.Icon(icon, size=60, color=color, opacity=0.3),
                    self.ft.Text(subtitle, color=self.ft.Colors.GREY_500, size=12),
                    self.ft.Container(expand=True),
                ], alignment=self.ft.MainAxisAlignment.CENTER, horizontal_alignment=self.ft.CrossAxisAlignment.CENTER),
                bgcolor="#111827",
                padding=20,
                border_radius=10,
                expand=1,
                border=self.ft.border.all(1, "#1E293B")
            )

        charts_row_1 = self.ft.Row([
            create_mock_chart("Sensor Data Distribution", "Gráfico de Pizza em breve", self.ft.Icons.PIE_CHART, self.ft.Colors.BLUE_400),
            create_mock_chart("Temperature per Hour", "Gráfico de Linha em breve", self.ft.Icons.SHOW_CHART, self.ft.Colors.CYAN_400),
            create_mock_chart("Distance traveled in seven days", "Gráfico de Barras em breve", self.ft.Icons.BAR_CHART, self.ft.Colors.BLUE_600),
        ], expand=True, spacing=20)

        charts_row_2 = self.ft.Row([
            create_mock_chart("Air Quality Status", "Métrica Detalhada", self.ft.Icons.AIR, self.ft.Colors.RED_400),
            create_mock_chart("Ammonia (NH3) Concentration", "Histórico de 24h", self.ft.Icons.SCATTER_PLOT, self.ft.Colors.PURPLE_400),
            create_mock_chart("Alcohol Variation", "Níveis de variação", self.ft.Icons.STACKED_BAR_CHART, self.ft.Colors.YELLOW_400),
        ], expand=True, spacing=20)

        # --- MONTAGEM DO LAYOUT FINAL (Apenas o conteúdo interno) ---
        area_dashboard = self.ft.Column([
            top_section,
            self.ft.Container(height=10),
            status_row,
            self.ft.Container(height=10),
            charts_row_1,
            charts_row_2
        ], expand=True, scroll=self.ft.ScrollMode.AUTO)

        # Dispara o popup
        self.mostrar_popup_pareamento()

        # Retorna o conteúdo ao invés de adicionar à page
        return area_dashboard