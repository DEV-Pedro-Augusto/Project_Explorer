class SpeedView:
    def __init__(self, system):
        self.system = system
        self.ft = system.ft

    def render(self):
        # Paleta de Cores (Dark Cyberpunk / Industrial)
        BG_CARD = "#111827"
        BORDER_COLOR = "#1f2937"
        ACCENT_CYAN = self.ft.Colors.CYAN_400
        ACCENT_AMBER = self.ft.Colors.AMBER_500
        
        return self.ft.Column([
            # 1. CABEÇALHO DO DASHBOARD
            self.ft.Row([
                self.ft.Column([
                    self.ft.Row([
                        self.ft.Icon(self.ft.Icons.DASHBOARD_ROUNDED, color=ACCENT_CYAN, size=32),
                        self.ft.Text("Mesa de Telemetria & Análise Avançada", size=28, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE)
                    ]),
                    self.ft.Text("Análise preditiva e diagnósticos com base no histórico do Supabase", color=self.ft.Colors.GREY_400, size=14)
                ]),
                # Filtro rápido por sessão (`id_sessoes_leituras`)
                self.ft.Dropdown(
                    label="Selecionar Sessão de Leituras",
                    width=250,
                    options=[
                        self.ft.dropdown.Option("Sessão #03 (Atual)"),
                        self.ft.dropdown.Option("Sessão #02 (25/05/2026)"),
                        self.ft.dropdown.Option("Sessão #01 (24/05/2026)"),
                    ],
                    border_color=BORDER_COLOR,
                    color=self.ft.Colors.WHITE,
                )
            ], alignment=self.ft.MainAxisAlignment.SPACE_BETWEEN),
            
            self.ft.Container(height=20),
            
            # 2. CARTÕES DE KPI (INDICADORES CHAVE DE PERFORMANCE)
            self.ft.ResponsiveRow([
                # KPI 1: Total de Registros na Sessão
                self.ft.Container(
                    col={"sm": 12, "md": 4},
                    bgcolor=BG_CARD, padding=20, border_radius=12, border=self.ft.border.all(1, BORDER_COLOR),
                    content=self.ft.Column([
                        self.ft.Text("Total de Leituras Coletadas", color=self.ft.Colors.GREY_500, size=12, weight=self.ft.FontWeight.BOLD),
                        self.ft.Text("1,420", size=32, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
                        self.ft.Row([self.ft.Icon(self.ft.Icons.TRENDING_UP, color=self.ft.Colors.GREEN_400, size=16), self.ft.Text("+12% vs. sessão anterior", color=self.ft.Colors.GREEN_400, size=12)])
                    ], spacing=5)
                ),
                # KPI 2: Sensores Ativos Detectados
                self.ft.Container(
                    col={"sm": 12, "md": 4},
                    bgcolor=BG_CARD, padding=20, border_radius=12, border=self.ft.border.all(1, BORDER_COLOR),
                    content=self.ft.Column([
                        self.ft.Text("Sensores Ativos na Tabela", color=self.ft.Colors.GREY_500, size=12, weight=self.ft.FontWeight.BOLD),
                        self.ft.Text("4 Sensores", size=32, weight=self.ft.FontWeight.BOLD, color=ACCENT_CYAN),
                        self.ft.Text("IDs: Ultra_01, Infra_L, Infra_R, Temp_M1", color=self.ft.Colors.GREY_400, size=12)
                    ], spacing=5)
                ),
                # KPI 3: Status de Consistência dos Dados
                self.ft.Container(
                    col={"sm": 12, "md": 4},
                    bgcolor=BG_CARD, padding=20, border_radius=12, border=self.ft.border.all(1, BORDER_COLOR),
                    content=self.ft.Column([
                        self.ft.Text("Latência Média de Escrita", color=self.ft.Colors.GREY_500, size=12, weight=self.ft.FontWeight.BOLD),
                        self.ft.Text("24 ms", size=32, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.GREEN_400),
                        self.ft.Row([self.ft.Icon(self.ft.Icons.CLOUD_DONE, color=self.ft.Colors.GREEN_400, size=16), self.ft.Text("Supabase Sync: Estável", color=self.ft.Colors.GREY_400, size=12)])
                    ], spacing=5)
                ),
            ], spacing=15),
            
            self.ft.Container(height=20),
            
            # 3. ÁREA DE ANÁLISE GRÁFICA / REPRODUÇÃO DAS LEITURAS
            self.ft.ResponsiveRow([
                # Painel de Monitoramento Gráfico Simulador
                self.ft.Container(
                    col={"sm": 12, "md": 8},
                    bgcolor=BG_CARD, padding=20, border_radius=12, border=self.ft.border.all(1, BORDER_COLOR),
                    content=self.ft.Column([
                        self.ft.Row([
                            self.ft.Text("Flutuação dos Valores Lidos por Carimbo de Tempo", size=16, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
                            self.ft.IconButton(icon=self.ft.Icons.REFRESH, icon_color=ACCENT_CYAN, tooltip="Atualizar do Banco")
                        ], alignment=self.ft.MainAxisAlignment.SPACE_BETWEEN),
                        self.ft.Container(height=10),
                        
                        # Aqui entra o componente LineChart do Flet populado com a sua coluna `valores_lidos` e `data_hora`
                        self.ft.Container(
                            height=200,
                            alignment=self.ft.alignment.center,
                            bgcolor="#1f2937",
                            border_radius=8,
                            content=self.ft.Text("[ Gráfico Dinâmico: Linha do Tempo de valores_lidos ]", color=self.ft.Colors.GREY_400)
                        ),
                        
                        # Legenda Dinâmica baseada no `id_etiquetas_sensores`
                        self.ft.Row([
                            self.ft.Row([self.ft.Container(width=12, height=12, bgcolor=self.ft.Colors.CYAN_400, border_radius=3), self.ft.Text("Ultra_01 (Proximidade)", size=12)]),
                            self.ft.Row([self.ft.Container(width=12, height=12, bgcolor=self.ft.Colors.AMBER_500, border_radius=3), self.ft.Text("Infra_L (Seguidor Linha)", size=12)]),
                            self.ft.Row([self.ft.Container(width=12, height=12, bgcolor=self.ft.Colors.PURPLE_400, border_radius=3), self.ft.Text("Temp_M1 (Temperatura)", size=12)]),
                        ], spacing=20)
                    ])
                ),
                
                # Painel Lateral: Log de Eventos Críticos (Anomalias detetadas no histórico)
                self.ft.Container(
                    col={"sm": 12, "md": 4},
                    bgcolor=BG_CARD, padding=20, border_radius=12, border=self.ft.border.all(1, BORDER_COLOR),
                    content=self.ft.Column([
                        self.ft.Text("Alertas de Anomalias", size=16, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
                        self.ft.Text("Filtro automático para valores_lidos fora do padrão seguro", size=12, color=self.ft.Colors.GREY_400),
                        self.ft.Container(height=5),
                        
                        # Lista de anomalias encontradas na tabela
                        self.ft.Column([
                            self.create_anomaly_item("12:34:11", "Ultra_01", "Valor Crítico: 3cm", self.ft.Colors.RED_ACCENT_400),
                            self.create_anomaly_item("12:35:45", "Temp_M1", "Pico detetado: 52°C", self.ft.Colors.ORANGE_400),
                            self.create_anomaly_item("12:39:02", "Infra_R", "Perda de leitura (Nulo)", self.ft.Colors.AMBER_400),
                        ], spacing=10, scroll=self.ft.ScrollMode.AUTO, height=180)
                    ])
                )
            ], spacing=15),
            
            self.ft.Container(height=20),
            
            # 4. TABELA DE DADOS BRUTOS (Inspecionador da Base de Dados)
            self.ft.Container(
                bgcolor=BG_CARD, padding=20, border_radius=12, border=self.ft.border.all(1, BORDER_COLOR),
                content=self.ft.Column([
                    self.ft.Row([
                        self.ft.Text("Últimos Registros Sincronizados (Tabela: LEITURAS)", size=16, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
                        self.ft.TextButton("Ver log completo", icon=self.ft.Icons.ARROW_FORWARD, icon_color=ACCENT_CYAN)
                    ], alignment=self.ft.MainAxisAlignment.SPACE_BETWEEN),
                    self.ft.Container(height=10),
                    
                    # Estrutura espelhada na imagem fornecida
                    self.ft.DataTable(
                        border=self.ft.border.all(1, "#1f2937"),
                        border_radius=8,
                        heading_row_color="#1f2937",
                        columns=[
                            self.ft.DataColumn(self.ft.Text("id_leituras", weight=self.ft.FontWeight.BOLD)),
                            self.ft.DataColumn(self.ft.Text("id_sessoes_leituras", weight=self.ft.FontWeight.BOLD)),
                            self.ft.DataColumn(self.ft.Text("id_etiquetas_sensores", weight=self.ft.FontWeight.BOLD)),
                            self.ft.DataColumn(self.ft.Text("valores_lidos", weight=self.ft.FontWeight.BOLD)),
                            self.ft.DataColumn(self.ft.Text("data_hora", weight=self.ft.FontWeight.BOLD)),
                        ],
                        rows=[
                            self.ft.DataRow(cells=[self.ft.DataCell(self.ft.Text("1")), self.ft.DataCell(self.ft.Text("Sessao_03")), self.ft.DataCell(self.ft.Text("Ultra_01")), self.ft.DataCell(self.ft.Text("24.5")), self.ft.DataCell(self.ft.Text("2026-05-26 20:30:11"))]),
                            self.ft.DataRow(cells=[self.ft.DataCell(self.ft.Text("2")), self.ft.DataCell(self.ft.Text("Sessao_03")), self.ft.DataCell(self.ft.Text("Infra_L")), self.ft.DataCell(self.ft.Text("1.0")), self.ft.DataCell(self.ft.Text("2026-05-26 20:30:12"))]),
                            self.ft.DataRow(cells=[self.ft.DataCell(self.ft.Text("3")), self.ft.DataCell(self.ft.Text("Sessao_03")), self.ft.DataCell(self.ft.Text("Temp_M1")), self.ft.DataCell(self.ft.Text("44.2")), self.ft.DataCell(self.ft.Text("2026-05-26 20:30:14"))]),
                        ]
                    )
                ])
            )
        ], expand=True, scroll=self.ft.ScrollMode.AUTO)

    def create_anomaly_item(self, timestamp, sensor, msg, icon_color):
        return self.ft.Container(
            padding=10, bgcolor="#1f2937", border_radius=6,
            content=self.ft.Row([
                self.ft.Icon(self.ft.Icons.REPORT_PROBLEM_ROUNDED, color=icon_color, size=18),
                self.ft.Column([
                    self.ft.Text(f"[{timestamp}] - Sensor: {sensor}", size=11, color=self.ft.Colors.GREY_400),
                    self.ft.Text(msg, size=13, weight=self.ft.FontWeight.W_500, color=self.ft.Colors.WHITE)
                ], spacing=2)
            ])
        )