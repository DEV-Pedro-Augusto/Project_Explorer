
import statistics

class SpeedView:
    def __init__(self, system):
        self.system = system
        self.ft = self.system.ft
        self.selected_session = None
        self.sessoes = []
        self.leituras = []
        self.anomalies = []

        self.total_readings_text = None
        self.sensor_count_text = None
        self.latest_timestamp_text = None
        self.session_dropdown = None
        self.data_table = None
        self.anomaly_column = None
        self.page_container = None
        self.view_mode = "overview"
        
        # --- NOVO: Referência para o componente de Gráfico ---
        self.chart = None

    def _format_datetime(self, timestamp_str):
        if not timestamp_str:
            return "N/A"
        try:
            return timestamp_str.replace("T", " ").replace("Z", "")
        except Exception:
            return str(timestamp_str)

    def _parse_float(self, value):
        try:
            if value is None:
                return None
            if isinstance(value, str):
                return float(value.replace(",", "."))
            return float(value)
        except Exception:
            return None

    def _load_sessions(self):
        try:
            id_usuario = self.system.obter_id_usuario()
            id_dispositivo = self.system.obter_id_dispositivo()
            if id_dispositivo:
                return self.system.model.database.listar_sessoes_leituras(id_dispositivo=id_dispositivo)
            return self.system.model.database.listar_sessoes_leituras(id_usuario=id_usuario)
        except Exception as e:
            print(f"Erro ao carregar sessões: {e}")
            return []

    def _load_readings(self, id_sessao=None):
        try:
            id_dispositivo = self.system.obter_id_dispositivo()
            if id_sessao is not None:
                try:
                    id_sessao = int(id_sessao)
                except Exception:
                    pass
            return self.system.model.database.listar_leituras(id_sessao=id_sessao, id_dispositivo=id_dispositivo)
        except Exception as e:
            print(f"Erro ao carregar leituras: {e}")
            return []

    def _build_session_options(self):
        options = []
        for sessao in self.sessoes:
            session_id = sessao.get("id_sessoes_leituras")
            display = f"Sessão {session_id} - {self._format_datetime(sessao.get('datas_uploads'))}"
            options.append(self.ft.dropdown.Option(key=str(session_id), text=display, data=session_id))
        return options

    def _detect_anomalies(self):
        values = [self._parse_float(l.get("valores_lidos")) for l in self.leituras]
        numeric_values = [v for v in values if v is not None]
        anomalies = []
        if numeric_values:
            mean = statistics.mean(numeric_values)
            stdev = statistics.stdev(numeric_values) if len(numeric_values) > 1 else 0
            threshold_high = mean + stdev * 2
            threshold_low = mean - stdev * 2
            for leitura in self.leituras:
                value = self._parse_float(leitura.get("valores_lidos"))
                if value is None:
                    anomalies.append((leitura, "Valor ausente ou inválido"))
                elif value > threshold_high:
                    anomalies.append((leitura, f"Valor acima do limite esperado ({value})"))
                elif value < threshold_low:
                    anomalies.append((leitura, f"Valor abaixo do limite esperado ({value})"))
        for leitura in self.leituras:
            if not leitura.get("data_hora"):
                anomalies.append((leitura, "Timestamp ausente"))
        return anomalies[:5]

    # --- NOVA FUNÇÃO: Mapeia self.leituras para pontos reais (X, Y) do gráfico ---
    def _build_chart_points(self):
        points = []
        # Inverte para que o gráfico corra em ordem cronológica (antigo -> recente)
        leituras_cronologicas = list(reversed(self.leituras))
        
        for index, leitura in enumerate(leituras_cronologicas):
            val = self._parse_float(leitura.get("valores_lidos"))
            if val is not None:
                points.append(self.ft.LineChartDataPoint(x=index, y=val))
        
        # Se não houver dados válidos, insere um ponto zero padrão para evitar travamentos
        if not points:
            points.append(self.ft.LineChartDataPoint(x=0, y=0))
        return points

    def _build_table_rows(self):
        rows = []
        if not self.leituras:
            rows.append(self.ft.DataRow(cells=[
                self.ft.DataCell(self.ft.Text("Sem dados", color=self.ft.Colors.GREY_500, size=11)),
                self.ft.DataCell(self.ft.Text("--", color=self.ft.Colors.GREY_500, size=11)),
                self.ft.DataCell(self.ft.Text("--", color=self.ft.Colors.GREY_500, size=11)),
                self.ft.DataCell(self.ft.Text("--", color=self.ft.Colors.GREY_500, size=11)),
                self.ft.DataCell(self.ft.Text("--", color=self.ft.Colors.GREY_500, size=11)),
            ]))
            return rows
        for leitura in self.leituras[:10]:
            rows.append(self.ft.DataRow(cells=[
                self.ft.DataCell(self.ft.Text(str(leitura.get("id_leituras", "-")), color=self.ft.Colors.WHITE70, size=11)),
                self.ft.DataCell(self.ft.Text(str(leitura.get("id_sessoes_leituras", "-")), color=self.ft.Colors.WHITE70, size=11)),
                self.ft.DataCell(self.ft.Text(str(leitura.get("id_etiquetas_sensores", "-")), color=self.ft.Colors.WHITE70, size=11)),
                self.ft.DataCell(self.ft.Text(str(leitura.get("valores_lidos", "-")), color=self.ft.Colors.WHITE70, size=11)),
                self.ft.DataCell(self.ft.Text(self._format_datetime(leitura.get("data_hora")), color=self.ft.Colors.WHITE70, size=11)),
            ]))
        return rows

    def _build_anomaly_controls(self):
        if not self.anomalies:
            return [self.ft.Text("Nenhuma anomalia detectada na sessão selecionada.", color=self.ft.Colors.GREEN_400, size=12)]
        controls = []
        for leitura, mensagem in self.anomalies:
            timestamp = self._format_datetime(leitura.get("data_hora"))
            sensor = leitura.get("id_etiquetas_sensores", "Desconhecido")
            controls.append(self.create_anomaly_item(timestamp, sensor, mensagem, self.ft.Colors.RED_ACCENT_400))
        return controls

    def _build_log_summary(self):
        if not self.leituras:
            return self.ft.Text("Nenhum registro encontrado para a sessão selecionada.", color=self.ft.Colors.GREY_400, size=12)

        numeric_values = [self._parse_float(l.get("valores_lidos")) for l in self.leituras]
        numeric_values = [v for v in numeric_values if v is not None]
        average_value = f"{statistics.mean(numeric_values):.2f}" if numeric_values else "N/A"
        min_value = f"{min(numeric_values):.2f}" if numeric_values else "N/A"
        max_value = f"{max(numeric_values):.2f}" if numeric_values else "N/A"
        first_ts = self._format_datetime(self.leituras[-1].get("data_hora")) if self.leituras else "N/A"
        last_ts = self._format_datetime(self.leituras[0].get("data_hora")) if self.leituras else "N/A"

        return self.ft.Column([
            self.ft.Text("Resumo do Log de Leituras", size=16, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            self.ft.Text(
                f"Sessão: {self.selected_session or 'N/A'} | Leituras: {len(self.leituras)} | Média: {average_value} | Mín: {min_value} | Máx: {max_value}",
                size=12, color=self.ft.Colors.GREY_400
            ),
            self.ft.Text(f"Período: {first_ts} → {last_ts}", size=12, color=self.ft.Colors.GREY_400),
        ], spacing=6)

    def _build_full_log_children(self):
        return [
            self.ft.Row([
                self.ft.Row([
                    self.ft.Icon(self.ft.Icons.LIST_ALT_ROUNDED, color=self.ft.Colors.CYAN_400, size=28),
                    self.ft.Text("Log completo de leituras", size=24, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
                ], alignment=self.ft.MainAxisAlignment.START),
                self.ft.TextButton("← Voltar", on_click=self._on_return_to_overview, style=self.ft.ButtonStyle(color=self.ft.Colors.GREY_200))
            ], alignment=self.ft.MainAxisAlignment.SPACE_BETWEEN),
            self.ft.Container(height=10),
            self._build_log_summary(),
            self.ft.Container(height=20),
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
                rows=self._build_table_rows(),
                expand=True,
            )
        ]

    def _on_view_full_log(self, e=None):
        self.view_mode = "full_log"
        self._refresh_data()
        if self.page_container is not None:
            self.page_container.controls = self._build_full_log_children()
            self.page_container.update()

    def _on_return_to_overview(self, e=None):
        self.view_mode = "overview"
        self._refresh_data()
        if self.page_container is not None:
            self.page_container.controls = self._build_overview_children()
            self.page_container.update()

    def _build_overview_children(self):
        return [
            self.ft.Row([
                self.ft.Column([
                    self.ft.Row([
                        self.ft.Icon(self.ft.Icons.DASHBOARD_ROUNDED, color=self.ft.Colors.CYAN_400, size=32),
                        self.ft.Text("Mesa de Telemetria & Análise Avançada", size=28, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE)
                    ]),
                    self.ft.Text("Dados reais carregados do banco de leituras e sessões.", color=self.ft.Colors.GREY_400, size=14)
                ]),
                self.session_dropdown
            ], alignment=self.ft.MainAxisAlignment.SPACE_BETWEEN),

            self.ft.Container(height=20),

            self.ft.ResponsiveRow([
                self.ft.Container(
                    col={"sm": 12, "md": 4},
                    bgcolor="#111827", padding=20, border_radius=12, border=self.ft.border.all(1, "#1f2937"),
                    content=self.ft.Column([
                        self.ft.Text("Total de Leituras", color=self.ft.Colors.GREY_500, size=12, weight=self.ft.FontWeight.BOLD),
                        self.total_readings_text,
                    ], spacing=5)
                ),
                self.ft.Container(
                    col={"sm": 12, "md": 4},
                    bgcolor="#111827", padding=20, border_radius=12, border=self.ft.border.all(1, "#1f2937"),
                    content=self.ft.Column([
                        self.ft.Text("Sensores na Sessão", color=self.ft.Colors.GREY_500, size=12, weight=self.ft.FontWeight.BOLD),
                        self.sensor_count_text,
                    ], spacing=5)
                ),
                self.ft.Container(
                    col={"sm": 12, "md": 4},
                    bgcolor="#111827", padding=20, border_radius=12, border=self.ft.border.all(1, "#1f2937"),
                    content=self.ft.Column([
                        self.ft.Text("Último Registro", color=self.ft.Colors.GREY_500, size=12, weight=self.ft.FontWeight.BOLD),
                        self.latest_timestamp_text,
                    ], spacing=5)
                ),
            ], spacing=15),

            self.ft.Container(height=20),

            self.ft.ResponsiveRow([
                self.ft.Container(
                    col={"sm": 12, "md": 8},
                    bgcolor="#111827", padding=20, border_radius=12, border=self.ft.border.all(1, "#1f2937"),
                    content=self.ft.Column([
                        self.ft.Row([
                            self.ft.Text("Visualização de Leituras por Tempo", size=16, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
                            self.ft.IconButton(icon=self.ft.Icons.REFRESH, icon_color=self.ft.Colors.CYAN_400, tooltip="Atualizar dados", on_click=self._on_session_change)
                        ], alignment=self.ft.MainAxisAlignment.SPACE_BETWEEN),
                        self.ft.Container(height=10),
                        
                        # --- MODIFICADO: Agora exibe o LineChart de verdade em vez do texto fixo ---
                        self.ft.Container(
                            height=200,
                            padding=15,
                            bgcolor="#1f2937",
                            border_radius=8,
                            content=self.chart
                        ),
                        
                        self.ft.Container(height=10),
                        self.ft.Row([
                            self.ft.Row([self.ft.Container(width=12, height=12, bgcolor=self.ft.Colors.CYAN_400, border_radius=3), self.ft.Text("Leitura Única", size=12)]),
                            self.ft.Row([self.ft.Container(width=12, height=12, bgcolor=self.ft.Colors.AMBER_500, border_radius=3), self.ft.Text("Sinal de Anomalia", size=12)])
                        ], spacing=20)
                    ])
                ),
                self.ft.Container(
                    col={"sm": 12, "md": 4},
                    bgcolor="#111827", padding=20, border_radius=12, border=self.ft.border.all(1, "#1f2937"),
                    content=self.ft.Column([
                        self.ft.Text("Alertas de Anomalias", size=16, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
                        self.ft.Text("Anomalias extraídas dos dados reais de leituras.", size=12, color=self.ft.Colors.GREY_400),
                        self.ft.Container(height=5),
                        self.anomaly_column
                    ])
                )
            ], spacing=15),

            self.ft.Container(height=20),

            self.ft.Container(
                bgcolor="#111827", padding=20, border_radius=12, border=self.ft.border.all(1, "#1f2937"),
                content=self.ft.Column([
                    self.ft.Row([
                        self.ft.Text("Últimos Registros Sincronizados (Tabela: LEITURAS)", size=16, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
                        self.ft.TextButton("Ver log completo", icon=self.ft.Icons.ARROW_FORWARD, icon_color=self.ft.Colors.CYAN_400, on_click=self._on_view_full_log)
                    ], alignment=self.ft.MainAxisAlignment.SPACE_BETWEEN),
                    self.ft.Container(height=10),
                    self.data_table
                ])
            )
        ]

    def _refresh_data(self):
        self.sessoes = self._load_sessions() or []
        if not self.selected_session and self.sessoes:
            self.selected_session = str(self.sessoes[0].get("id_sessoes_leituras"))
        self.leituras = self._load_readings(self.selected_session) or []
        self.total_readings = len(self.leituras)
        self.sensor_count = len({l.get("id_etiquetas_sensores") for l in self.leituras if l.get("id_etiquetas_sensores")})
        self.latest_timestamp = self._format_datetime(self.leituras[0].get("data_hora")) if self.leituras else "N/A"
        self.anomalies = self._detect_anomalies()

    def _on_session_change(self, e=None):
        if e is not None:
            if hasattr(e, "control") and getattr(e.control, "value", None) is not None:
                self.selected_session = str(e.control.value)
            elif hasattr(e, "control") and getattr(e.control, "data", None) is not None:
                self.selected_session = str(e.control.data)
            elif getattr(e, "value", None) is not None:
                self.selected_session = str(e.value)

        self._refresh_data()
        
        # --- MODIFICADO: Atualiza dinamicamente os pontos do gráfico ao trocar de sessão ---
        if self.chart:
            self.chart.data_series[0].data_points = self._build_chart_points()
            self.chart.update()

        if self.session_dropdown:
            self.session_dropdown.value = self.selected_session
            self.session_dropdown.update()
        if self.total_readings_text:
            self.total_readings_text.value = str(self.total_readings)
            self.total_readings_text.update()
        if self.sensor_count_text:
            self.sensor_count_text.value = f"{self.sensor_count} sensor(es)"
            self.sensor_count_text.update()
        if self.latest_timestamp_text:
            self.latest_timestamp_text.value = self.latest_timestamp
            self.latest_timestamp_text.update()
        if self.data_table:
            self.data_table.rows = self._build_table_rows()
            self.data_table.update()
        if self.anomaly_column:
            self.anomaly_column.controls = self._build_anomaly_controls()
            self.anomaly_column.update()
        self.system.page.update()

    def render(self):
        BG_CARD = "#111827"
        BORDER_COLOR = "#1f2937"
        ACCENT_CYAN = self.ft.Colors.CYAN_400
        ACCENT_AMBER = self.ft.Colors.AMBER_500

        self._refresh_data()

        # --- NOVO: Inicialização do LineChart estruturado dentro do render ---
        self.chart = self.ft.LineChart(
            data_series=[
                self.ft.LineChartData(
                    data_points=self._build_chart_points(),
                    stroke_width=3,
                    color=ACCENT_CYAN,
                    curved=True,
                    below_line_bgcolor=self.ft.Colors.with_opacity(0.1, ACCENT_CYAN),
                )
            ],
            border=self.ft.border.all(1, "#1E293B"),
            horizontal_grid_lines=self.ft.ChartGridLines(color="#1E293B", interval=10),
            vertical_grid_lines=self.ft.ChartGridLines(color="#1E293B", interval=1),
            animate=300 # Transição suave ao mudar os dados
        )

        self.session_dropdown = self.ft.Dropdown(
            label="Selecionar Sessão de Leituras",
            width=300,
            options=self._build_session_options(),
            value=self.selected_session,
            border_color=BORDER_COLOR,
            color=self.ft.Colors.WHITE,
            on_change=self._on_session_change,
        )

        self.total_readings_text = self.ft.Text(str(self.total_readings), size=32, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE)
        self.sensor_count_text = self.ft.Text(f"{self.sensor_count} sensor(es)", size=32, weight=self.ft.FontWeight.BOLD, color=ACCENT_CYAN)
        self.latest_timestamp_text = self.ft.Text(self.latest_timestamp, size=20, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.GREEN_400)

        self.data_table = self.ft.DataTable(
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
            rows=self._build_table_rows(),
            expand=True,
        )

        self.anomaly_column = self.ft.Column(self._build_anomaly_controls(), spacing=10)

        if self.page_container is None:
            self.page_container = self.ft.Column(
                self._build_overview_children() if self.view_mode == "overview" else self._build_full_log_children(),
                expand=True,
                scroll=self.ft.ScrollMode.AUTO
            )
        else:
            self.page_container.controls = self._build_overview_children() if self.view_mode == "overview" else self._build_full_log_children()

        return self.page_container

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