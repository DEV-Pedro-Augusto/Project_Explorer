from datetime import datetime

class DashboardView:
    def __init__(self, system, nome_carrinho):
        self.system = system
        self.nome_carrinho = nome_carrinho
        self.ft = self.system.ft
        self.db_client = system.model.database if hasattr(system.model, 'database') else None
        self.sensores_map = {}  # Cache do mapeamento de sensores
        self._load_sensores_map()

    def _load_sensores_map(self):
        """Carrega o mapeamento de sensores do banco para usar no dashboard."""
        if not self.db_client:
            return
        
        try:
            # Obtém o ID do dispositivo selecionado
            id_dispositivo = self.system.obter_id_dispositivo()
            
            if not id_dispositivo:
                print("Nenhum dispositivo selecionado para carregar sensores")
                return
            
            # Carrega apenas os sensores deste dispositivo
            sensores_db = self.db_client.listar_sensores_dispositivo(id_dispositivo)
            
            # Mapeia os sensores com ícones e cores
            mapeamento_sensores = {
                "mq-2": {"icon": self.ft.Icons.CLOUD, "color": self.ft.Colors.GREEN_400, "nome_display": "MQ2 (Gás)"},
                "mq-3": {"icon": self.ft.Icons.LOCAL_DRINK, "color": self.ft.Colors.YELLOW_700, "nome_display": "MQ3 (Álcool)"},
                "mq-7": {"icon": self.ft.Icons.SMOKE_FREE, "color": self.ft.Colors.RED_500, "nome_display": "MQ7 (CO)"},
                "mocr": {"icon": self.ft.Icons.OPACITY, "color": self.ft.Colors.ORANGE_400, "nome_display": "MOCR (Odometria)"},
                "hc-sr": {"icon": self.ft.Icons.STRAIGHTEN, "color": self.ft.Colors.BLUE_400, "nome_display": "HC-SR04 (Ultrassônico)"},
                "temperatura": {"icon": self.ft.Icons.THERMOSTAT, "color": self.ft.Colors.RED_400, "nome_display": "Temperatura"},
                "umidade": {"icon": self.ft.Icons.WATER_DROP, "color": self.ft.Colors.CYAN_400, "nome_display": "Umidade"},
                "distancia": {"icon": self.ft.Icons.STRAIGHTEN, "color": self.ft.Colors.BLUE_300, "nome_display": "Distância"},
                "luz": {"icon": self.ft.Icons.WB_SUNNY, "color": self.ft.Colors.YELLOW_400, "nome_display": "Luminosidade"},
                "pressao": {"icon": self.ft.Icons.SPEED, "color": self.ft.Colors.PURPLE_400, "nome_display": "Pressão"},
            }
            
            # Mapeamento por ID para sensores genéricos
            mapeamento_id_sensores = {
                6: {"icon": self.ft.Icons.WATER_DROP, "color": self.ft.Colors.CYAN_400, "nome_display": "Umidade"},
                7: {"icon": self.ft.Icons.STRAIGHTEN, "color": self.ft.Colors.BLUE_300, "nome_display": "Distância"},
                8: {"icon": self.ft.Icons.THERMOSTAT, "color": self.ft.Colors.RED_400, "nome_display": "Temperatura"},
            }
            
            for sensor in sensores_db:
                id_sensor = sensor.get('id_sensores')
                nome_sensor = sensor.get('nomes_sensores', '').lower()
                
                tipo_info = None
                
                # Primeiro tenta identificar por nome
                for chave, info in mapeamento_sensores.items():
                    if chave in nome_sensor:
                        tipo_info = info
                        break
                
                # Se não identificou por nome, tenta por ID
                if not tipo_info and id_sensor in mapeamento_id_sensores:
                    tipo_info = mapeamento_id_sensores[id_sensor]
                
                if not tipo_info:
                    tipo_info = {"icon": self.ft.Icons.SENSORS_OUTLINED, "color": self.ft.Colors.BLUE_300, "nome_display": f"Sensor {id_sensor}"}
                
                self.sensores_map[id_sensor] = tipo_info
                
        except Exception as e:
            print(f"Erro ao carregar mapeamento de sensores: {e}")

    def _get_sensor_info(self, id_sensor):
        """Retorna informações do sensor (nome, ícone, cor) baseado no ID."""
        if id_sensor in self.sensores_map:
            return self.sensores_map[id_sensor]
        # Padrão se não encontrar
        return {"icon": self.ft.Icons.SPEED, "color": self.ft.Colors.GREY_400, "nome_display": f"Sensor {id_sensor}"}

    def mostrar_popup_pareamento(self):
        dlg = self.ft.AlertDialog(
            title=self.ft.Text("Pareamento Necessário", weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            content=self.ft.Text(f"Use este código no {self.nome_carrinho} para sincronizar:\n\n[ OI ]", size=18, text_align=self.ft.TextAlign.CENTER),
            actions=[
                self.ft.ElevatedButton("Entendi e Conectei", on_click=lambda e: self.fechar_popup(dlg), bgcolor=self.ft.Colors.BLUE_600, color=self.ft.Colors.WHITE)
            ],
            bgcolor="#121826",
            shape=self.ft.RoundedRectangleBorder(radius=10)
        )
        self.system.page.dialog = dlg
        dlg.open = True
        self.system.page.update()

    def fechar_popup(self, dlg):
        dlg.open = False
        self.system.page.update()

    def _format_timestamp(self, timestamp_str):
        if not timestamp_str:
            return "N/A"
        try:
            return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')).strftime("%d/%m %H:%M")
        except Exception:
            return str(timestamp_str)[:19]

    def _load_sessoes(self):
        try:
            id_usuario = self.system.obter_id_usuario()
            id_dispositivo = self.system.obter_id_dispositivo()
            if id_dispositivo:
                sessoes = self.system.model.database.listar_sessoes_leituras(id_dispositivo=id_dispositivo)
            else:
                sessoes = self.system.model.database.listar_sessoes_leituras(id_usuario=id_usuario)
            return sessoes or []
        except Exception as e:
            print(f"Erro ao carregar sessões do dashboard: {e}")
            return []

    def _load_session_readings(self, id_sessao):
        if not id_sessao:
            return []
        try:
            return self.system.model.database.listar_leituras(id_sessao=id_sessao) or []
        except Exception as e:
            print(f"Erro ao carregar leituras do dashboard: {e}")
            return []

    def _carregar_dados_consolidados(self):
        """Carrega dados consolidados das etiquetas de sensores"""
        try:
            id_dispositivo = self.system.obter_id_dispositivo()
            if not id_dispositivo:
                return []
            
            # Carrega as leituras do dispositivo
            leituras = self.system.model.database.listar_leituras(id_dispositivo=id_dispositivo)
            
            if not leituras:
                return []
            
            # Mapeamento inverso de etiquetas
            mapeamento_reverso = {
                1: {"nome": "MQ2 (PPM)", "unidade": "PPM"},
                2: {"nome": "MQ2 (LEL %)", "unidade": "%"},
                3: {"nome": "MQ3 (PPM)", "unidade": "PPM"},
                4: {"nome": "MQ3 (mg/L)", "unidade": "MG/L"},
                5: {"nome": "MQ7 (PPM)", "unidade": "PPM"},
                6: {"nome": "MQ7 (COHB %)", "unidade": "%"},
                7: {"nome": "Tempo de Volta", "unidade": "S"},
                8: {"nome": "Distância Total", "unidade": "M"},
                9: {"nome": "Sensor Frente", "unidade": "CM"},
                10: {"nome": "Sensor Direita", "unidade": "CM"},
                11: {"nome": "Sensor Esquerda", "unidade": "CM"},
                12: {"nome": "Sensor Traseira", "unidade": "CM"},
            }
            
            # Mapeamento de ícones
            mapeamento_icones = {
                "mq2": {"icon": self.ft.Icons.CLOUD, "color": self.ft.Colors.GREEN_400},
                "mq3": {"icon": self.ft.Icons.LOCAL_DRINK, "color": self.ft.Colors.YELLOW_700},
                "mq7": {"icon": self.ft.Icons.SMOKE_FREE, "color": self.ft.Colors.RED_500},
                "mocr": {"icon": self.ft.Icons.OPACITY, "color": self.ft.Colors.ORANGE_400},
                "hc-sr": {"icon": self.ft.Icons.STRAIGHTEN, "color": self.ft.Colors.BLUE_400},
                "tempo": {"icon": self.ft.Icons.SCHEDULE, "color": self.ft.Colors.PURPLE_400},
                "distancia": {"icon": self.ft.Icons.STRAIGHTEN, "color": self.ft.Colors.BLUE_300},
            }
            
            # Agrupa por etiqueta e calcula a média
            dados_consolidados = {}
            for leitura in leituras:
                id_etiqueta = leitura.get('id_etiquetas_sensores')
                valor = leitura.get('valores_lidos')
                
                if id_etiqueta and valor is not None:
                    try:
                        valor_num = float(valor)
                        if id_etiqueta not in dados_consolidados:
                            dados_consolidados[id_etiqueta] = {'valores': []}
                        dados_consolidados[id_etiqueta]['valores'].append(valor_num)
                    except Exception:
                        pass
            
            # Calcula a média e prepara os dados
            resultado = []
            
            for id_etiqueta, dados in dados_consolidados.items():
                if dados['valores']:
                    media = sum(dados['valores']) / len(dados['valores'])
                    
                    # Busca info da etiqueta no mapeamento
                    info_etiqueta = mapeamento_reverso.get(id_etiqueta, {})
                    nome = info_etiqueta.get('nome', f'Etiqueta {id_etiqueta}')
                    unidade = info_etiqueta.get('unidade', '')
                    
                    # Encontra o ícone apropriado
                    icon_info = None
                    nome_lower = nome.lower()
                    for chave, info in mapeamento_icones.items():
                        if chave in nome_lower:
                            icon_info = info
                            break
                    
                    if not icon_info:
                        icon_info = {"icon": self.ft.Icons.SENSORS_OUTLINED, "color": self.ft.Colors.BLUE_300}
                    
                    resultado.append({
                        'id': id_etiqueta,
                        'nome': nome[:25],
                        'valor': f"{media:.2f}",
                        'unidade': unidade,
                        'icon': icon_info['icon'],
                        'color': icon_info['color']
                    })
            
            return resultado
        except Exception as e:
            print(f"Erro ao carregar dados consolidados: {e}")
            return []

    def _build_sensor_badges(self, leituras):
        latest_by_sensor = {}
        for leitura in leituras:
            sensor = leitura.get('id_etiquetas_sensores', 'Desconhecido')
            ts = leitura.get('data_hora')
            if sensor not in latest_by_sensor or (ts and latest_by_sensor[sensor].get('data_hora', '') < ts):
                latest_by_sensor[sensor] = leitura

        badges = []

        for idx, (sensor, leitura) in enumerate(list(latest_by_sensor.items())):
            value = leitura.get('valores_lidos', 0)
            
            # Filtra sensores com valor 0 ou vazio
            try:
                valor_numerico = float(value) if value else 0
                if valor_numerico == 0:
                    continue  # Pula sensores com valor 0
            except (ValueError, TypeError):
                continue  # Pula valores inválidos
            
            # Obtém informações do sensor do mapeamento
            sensor_info = self._get_sensor_info(sensor)
            icon = sensor_info.get("icon", self.ft.Icons.SPEED)
            color = sensor_info.get("color", self.ft.Colors.GREY_400)
            nome = sensor_info.get("nome_display", f"Sensor {sensor}")
            
            # Encapsulado em um Container com largura definida para alinhar perfeitamente na Grid
            badges.append(
                self.ft.Container(
                    content=self.ft.Row([
                        self.ft.Container(
                            content=self.ft.Icon(icon, color=color, size=24),
                            padding=6,
                            border=self.ft.border.all(1, color),
                            border_radius=8,
                            bgcolor="#0A1122"
                        ),
                        self.ft.Column([
                            self.ft.Row([
                                self.ft.Text(str(value), size=18, weight=self.ft.FontWeight.W_900, color=self.ft.Colors.WHITE),
                            ], spacing=2),
                            self.ft.Text(nome, size=11, color=self.ft.Colors.GREY_500)
                        ], spacing=0, alignment=self.ft.MainAxisAlignment.CENTER)
                    ], spacing=8),
                    bgcolor="#111827",
                    padding=10,
                    border_radius=8,
                    border=self.ft.border.all(1, "#1f2937"),
                )
            )
            
        if not badges:
            return [self.ft.Text("Nenhuma leitura na última sessão.", color=self.ft.Colors.GREY_500, size=13)]
        return badges

    def _build_line_chart(self, leituras):
        if not leituras:
            return self.ft.Text("Aguardando dados numéricos...", color=self.ft.Colors.GREY_500, size=12)

        leituras_cronologicas = sorted(leituras, key=lambda l: l.get('data_hora') or '')[-8:]
        data_points = []
        for idx, l in enumerate(leituras_cronologicas):
            try:
                data_points.append(self.ft.LineChartDataPoint(idx, float(l.get('valores_lidos', 0))))
            except ValueError:
                continue

        if not data_points:
            return self.ft.Text("Sem dados convertíveis para gráfico", color=self.ft.Colors.GREY_500, size=12)

        return self.ft.LineChart(
            data_series=[
                self.ft.LineChartData(
                    data_points=data_points,
                    stroke_width=3,
                    color=self.ft.Colors.CYAN_400,
                    curved=True,
                    below_line_bgcolor=self.ft.Colors.with_opacity(0.1, self.ft.Colors.CYAN_400),
                )
            ],
            border=self.ft.border.all(1, "#1E293B"),
            horizontal_grid_lines=self.ft.BorderSide(1, "#1E293B"),
            vertical_grid_lines=self.ft.BorderSide(1, "#1E293B"),
            expand=True
        )

    def _build_bar_chart(self, leituras):
        if not leituras:
            return self.ft.Text("Aguardando dados...", color=self.ft.Colors.GREY_500, size=12)

        sensor_counts = {}
        for l in leituras:
            s = l.get('id_etiquetas_sensores', 'Sensor')
            sensor_counts[s] = sensor_counts.get(s, 0) + 1

        bar_groups = []
        for idx, (sensor, count) in enumerate(list(sensor_counts.items())[:4]):
            bar_groups.append(
                self.ft.BarChartGroup(
                    x=idx,
                    bar_rods=[self.ft.BarChartRod(from_y=0, to_y=count, width=16, color=self.ft.Colors.BLUE_400, border_radius=4)]
                )
            )

        if not bar_groups:
            return self.ft.Text("Sem dados de sensores", color=self.ft.Colors.GREY_500, size=12)

        return self.ft.BarChart(
            bar_groups=bar_groups,
            border=self.ft.border.all(1, "#1E293B"),
            expand=True
        )

    def _build_readings_rows(self, leituras):
        rows = []
        if not leituras:
            rows.append(self.ft.DataRow(cells=[
                self.ft.DataCell(self.ft.Text("Sem leituras", color=self.ft.Colors.GREY_500, size=11)),
                self.ft.DataCell(self.ft.Text("--", color=self.ft.Colors.GREY_500, size=11)),
                self.ft.DataCell(self.ft.Text("--", color=self.ft.Colors.GREY_500, size=11)),
                self.ft.DataCell(self.ft.Text("--", color=self.ft.Colors.GREY_500, size=11)),
                self.ft.DataCell(self.ft.Text("--", color=self.ft.Colors.GREY_500, size=11)),
            ]))
            return rows

        leituras_ordenadas = sorted(leituras, key=lambda l: l.get('data_hora') or '', reverse=True)
        for leitura in leituras_ordenadas[:12]: 
            rows.append(self.ft.DataRow(cells=[
                self.ft.DataCell(self.ft.Text(self._format_timestamp(leitura.get('data_hora')), color=self.ft.Colors.WHITE70, size=11)),
                self.ft.DataCell(self.ft.Text(str(leitura.get('id_sessoes_leituras', '-')), color=self.ft.Colors.WHITE70, size=11)),
                self.ft.DataCell(self.ft.Text(str(leitura.get('id_etiquetas_sensores', '-')), color=self.ft.Colors.WHITE70, size=11)),
                self.ft.DataCell(self.ft.Text(str(leitura.get('valores_lidos', '-')), color=self.ft.Colors.CYAN_400, size=11, weight=self.ft.FontWeight.BOLD)),
                self.ft.DataCell(self.ft.Text(str(leitura.get('id_leituras', '-')), color=self.ft.Colors.WHITE70, size=11)),
            ]))
        return rows

    def _build_pie_chart(self, leituras):
        """Gráfico de pizza mostrando distribuição de sensores"""
        if not leituras:
            return self.ft.Text("Aguardando dados...", color=self.ft.Colors.GREY_500, size=12)

        # Mapeamento de etiquetas
        mapeamento_sensores = {
            1: "MQ2 (PPM)",
            2: "MQ2 (LEL %)",
            3: "MQ3 (PPM)",
            4: "MQ3 (mg/L)",
            5: "MQ7 (PPM)",
            6: "MQ7 (COHB %)",
            7: "Tempo de Volta",
            8: "Distância Total",
            9: "Sensor Frente",
            10: "Sensor Direita",
            11: "Sensor Esquerda",
            12: "Sensor Traseira",
        }

        sensor_counts = {}
        for l in leituras:
            sensor_id = l.get('id_etiquetas_sensores', 'Sensor')
            sensor_counts[sensor_id] = sensor_counts.get(sensor_id, 0) + 1

        if not sensor_counts:
            return self.ft.Text("Sem dados de sensores", color=self.ft.Colors.GREY_500, size=12)

        pie_sections = []
        colors = [
            self.ft.Colors.CYAN_400,
            self.ft.Colors.GREEN_400,
            self.ft.Colors.ORANGE_400,
            self.ft.Colors.RED_400,
            self.ft.Colors.PURPLE_400,
            self.ft.Colors.BLUE_400,
        ]
        
        for idx, (sensor_id, count) in enumerate(list(sensor_counts.items())[:6]):
            sensor_nome = mapeamento_sensores.get(sensor_id, f"Sensor {sensor_id}")
            pie_sections.append(
                self.ft.PieChartSection(
                    value=count,
                    title=f"{sensor_nome}\n({count})",
                    title_style=self.ft.TextStyle(color=self.ft.Colors.WHITE, size=12, weight=self.ft.FontWeight.BOLD),
                    color=colors[idx % len(colors)],
                )
            )

        return self.ft.PieChart(sections=pie_sections, expand=True)

    def _build_max_min_chart(self, leituras):
        """Gráfico mostrando máximo e mínimo de cada sensor"""
        if not leituras:
            return self.ft.Text("Aguardando dados...", color=self.ft.Colors.GREY_500, size=12)

        sensor_stats = {}
        for l in leituras:
            sensor_id = l.get('id_etiquetas_sensores', 'Sensor')
            try:
                valor = float(l.get('valores_lidos', 0))
                if sensor_id not in sensor_stats:
                    sensor_stats[sensor_id] = {'max': valor, 'min': valor, 'count': 0}
                else:
                    sensor_stats[sensor_id]['max'] = max(sensor_stats[sensor_id]['max'], valor)
                    sensor_stats[sensor_id]['min'] = min(sensor_stats[sensor_id]['min'], valor)
                sensor_stats[sensor_id]['count'] += 1
            except ValueError:
                continue

        if not sensor_stats:
            return self.ft.Text("Sem dados válidos", color=self.ft.Colors.GREY_500, size=12)

        bar_groups = []
        for idx, (sensor, stats) in enumerate(list(sensor_stats.items())[:4]):
            bar_groups.append(
                self.ft.BarChartGroup(
                    x=idx,
                    bar_rods=[
                        self.ft.BarChartRod(from_y=0, to_y=stats['max'], width=8, color=self.ft.Colors.RED_400, border_radius=2),
                        self.ft.BarChartRod(from_y=0, to_y=stats['min'], width=8, color=self.ft.Colors.GREEN_400, border_radius=2),
                    ]
                )
            )

        return self.ft.BarChart(
            bar_groups=bar_groups,
            border=self.ft.border.all(1, "#1E293B"),
            expand=True
        )

    def render(self):
        BG_CARD = "#111827"
        BORDER_COLOR = "#1f2937"
        ACCENT_CYAN = self.ft.Colors.CYAN_400

        sessoes = self._load_sessoes()
        total_sessoes = len(sessoes)
        em_andamento = sum(1 for s in sessoes if not s.get('fim_missao'))
        ultima_sessao = sessoes[0] if sessoes else None
        ultimo_id_sessao = ultima_sessao.get('id_sessoes_leituras') if ultima_sessao else None
        
        leituras = self._load_session_readings(ultimo_id_sessao)
        total_leituras = len(leituras)
        ultima_atualizacao = self._format_timestamp(leituras[0].get('data_hora')) if leituras else "N/A"
        
        descricao_sessao = ultima_sessao.get('descricao_livre', 'Sem descrição') if ultima_sessao else 'Nenhuma sessão ativa'
        inicio_sessao = self._format_timestamp(ultima_sessao.get('inicio_missao')) if ultima_sessao else 'N/A'
        fim_sessao = self._format_timestamp(ultima_sessao.get('fim_missao')) if ultima_sessao and ultima_sessao.get('fim_missao') else 'Em andamento'

        # 1. Header
        header = self.ft.Row([
            self.ft.Column([
                self.ft.Row([
                    self.ft.Icon(self.ft.Icons.DASHBOARD_ROUNDED, color=ACCENT_CYAN, size=32),
                    self.ft.Text(f"Dashboard do {self.nome_carrinho}", size=28, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE)
                ], spacing=10),
                self.ft.Text("Métricas de telemetria integradas em tempo real com o banco de dados.", color=self.ft.Colors.GREY_400, size=14)
            ]),
            self.ft.IconButton(
                icon=self.ft.Icons.REFRESH_ROUNDED,
                icon_color=ACCENT_CYAN,
                tooltip="Atualizar dashboard",
                on_click=lambda e: self.system.atualizar_tela() if hasattr(self.system, 'atualizar_tela') else None
            )
        ], alignment=self.ft.MainAxisAlignment.SPACE_BETWEEN)

        # 1.5 PAINEL DE DADOS CONSOLIDADOS DOS SENSORES
        dados_consolidados = self._carregar_dados_consolidados()
        cards_sensores_consolidados = []
        for dado in dados_consolidados:
            card_sensor = self.ft.Container(
                content=self.ft.Column([
                    self.ft.Row([
                        self.ft.Icon(dado['icon'], color=dado['color'], size=28),
                        self.ft.Text(f"{dado['valor']}", size=18, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE)
                    ], alignment=self.ft.MainAxisAlignment.CENTER, spacing=8),
                    self.ft.Container(height=4),
                    self.ft.Text(f"{dado['nome'][:20]}", size=10, color=self.ft.Colors.GREY_400, text_align=self.ft.TextAlign.CENTER),
                    self.ft.Text(f"{dado['unidade']}", size=8, color=self.ft.Colors.GREY_500, text_align=self.ft.TextAlign.CENTER)
                ], horizontal_alignment=self.ft.CrossAxisAlignment.CENTER, alignment=self.ft.MainAxisAlignment.CENTER),
                width=120,
                height=110,
                padding=10,
                bgcolor="#141E30",
                border=self.ft.border.all(1, "#243B55"),
                border_radius=10
            )
            cards_sensores_consolidados.append(card_sensor)
        
        painel_dados_consolidados = self.ft.Container(
            content=self.ft.Column([
                self.ft.Text("Dados Consolidados dos Sensores", size=14, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
                self.ft.Container(height=8),
                self.ft.Row(
                    cards_sensores_consolidados or [self.ft.Text("Nenhum dado disponível", color=self.ft.Colors.GREY_500)],
                    scroll=self.ft.ScrollMode.AUTO,
                    spacing=10
                )
            ], spacing=8),
            padding=15,
            bgcolor="#0B132B",
            border_radius=10,
            border=self.ft.border.all(1, "#1E293B")
        ) if cards_sensores_consolidados else self.ft.Container()

        # 2. Seção Superior
        session_info_card = self.ft.Container(
            content=self.ft.Column([
                self.ft.Row([
                    self.ft.Icon(self.ft.Icons.SATELLITE_ALT_ROUNDED, color=ACCENT_CYAN, size=20),
                    self.ft.Text(f"SESSÃO ATIVA #{ultimo_id_sessao or 'N/A'}", weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE, size=14)
                ]),
                self.ft.Text(descricao_sessao, color=self.ft.Colors.GREY_300, size=12, max_lines=2),
                self.ft.Text(f"Período: {inicio_sessao} → {fim_sessao}", size=11, color=self.ft.Colors.GREY_500)
            ], spacing=5),
            bgcolor="#0B132B", 
            padding=15,
            border_radius=10,
            border=self.ft.border.all(1, "#1E293B"),
            expand=3
        )

        top_section = self.ft.Row([session_info_card], spacing=20, vertical_alignment=self.ft.CrossAxisAlignment.START, expand=True)

        # 3. Linha do Meio
        def create_info_card(title, value, icon_name=None, highlight=False):
            return self.ft.Container(
                content=self.ft.Column([
                    self.ft.Row([
                        self.ft.Icon(icon_name, size=16, color=self.ft.Colors.GREY_400) if icon_name else self.ft.Container(),
                        self.ft.Text(title, color=self.ft.Colors.GREY_400, size=13)
                    ]),
                    self.ft.Text(value, color=self.ft.Colors.WHITE, size=20, weight=self.ft.FontWeight.BOLD)
                ], spacing=10),
                bgcolor="#0B1A40" if highlight else BG_CARD,
                padding=20,
                border_radius=10,
                border=self.ft.border.all(1, BORDER_COLOR),
                expand=1
            )

        status_row = self.ft.Row([
            create_info_card("Sessões Registradas", f"{total_sessoes}", self.ft.Icons.HISTORY_TOGGLE_OFF_ROUNDED),
            create_info_card("Em Andamento", f"{em_andamento}", self.ft.Icons.PLAY_CIRCLE_OUTLINE, highlight=True),
            create_info_card("Leituras da Sessão", f"{total_leituras}", self.ft.Icons.SPEED),
            create_info_card("Última Sincronização", ultima_atualizacao, self.ft.Icons.FACT_CHECK_OUTLINED),
        ], spacing=20)

        # 4. DUAS LINHAS DE GRÁFICOS
        charts_row_1 = self.ft.Row([
            self.ft.Container(
                content=self.ft.Column([
                    self.ft.Text("Máximos e Mínimos por Sensor", color=self.ft.Colors.WHITE, size=14, weight=self.ft.FontWeight.W_500),
                    self.ft.Container(height=5),
                    self._build_max_min_chart(leituras),
                ]),
                bgcolor=BG_CARD, padding=20, border_radius=10, border=self.ft.border.all(1, "#1E293B"), height=220, expand=1
            ),
            self.ft.Container(
                content=self.ft.Column([
                    self.ft.Text("Volume de Registros por Sensor (Barras)", color=self.ft.Colors.WHITE, size=14, weight=self.ft.FontWeight.W_500),
                    self.ft.Container(height=5),
                    self._build_bar_chart(leituras),
                ]),
                bgcolor=BG_CARD, padding=20, border_radius=10, border=self.ft.border.all(1, "#1E293B"), height=220, expand=1
            )
        ], spacing=20)

        # 5. SEGUNDA LINHA DE GRÁFICOS (Aumentados para melhor legibilidade)
        charts_row_2 = self.ft.Column([
            self.ft.Row([
                self.ft.Container(
                    content=self.ft.Column([
                        self.ft.Text("Distribuição de Sensores (Pizza)", color=self.ft.Colors.WHITE, size=15, weight=self.ft.FontWeight.BOLD),
                        self.ft.Container(height=8),
                        self._build_pie_chart(leituras),
                    ]),
                    bgcolor=BG_CARD, padding=20, border_radius=10, border=self.ft.border.all(1, "#1E293B"), height=350, expand=1
                ),
            ], spacing=20),
            self.ft.Row([
                self.ft.Container(
                    content=self.ft.Column([
                        self.ft.Text("Variação Temporal de Leituras (Linha)", color=self.ft.Colors.WHITE, size=15, weight=self.ft.FontWeight.BOLD),
                        self.ft.Container(height=8),
                        self._build_line_chart(leituras),
                    ]),
                    bgcolor=BG_CARD, padding=20, border_radius=10, border=self.ft.border.all(1, "#1E293B"), height=280, expand=1
                )
            ], spacing=20)
        ], spacing=15)

        # Tabela de Histórico
        readings_table = self.ft.DataTable(
            border=self.ft.border.all(1, BORDER_COLOR),
            border_radius=10,
            heading_row_color="#1f2937",
            columns=[
                self.ft.DataColumn(self.ft.Text("Hora", color=self.ft.Colors.CYAN_400, size=12, weight=self.ft.FontWeight.BOLD)),
                self.ft.DataColumn(self.ft.Text("Sessão", color=self.ft.Colors.WHITE, size=12)),
                self.ft.DataColumn(self.ft.Text("Sensor", color=self.ft.Colors.WHITE, size=12)),
                self.ft.DataColumn(self.ft.Text("Valor Lido", color=self.ft.Colors.WHITE, size=12)),
                self.ft.DataColumn(self.ft.Text("ID Registro", color=self.ft.Colors.WHITE, size=12)),
            ],
            rows=self._build_readings_rows(leituras),
            bgcolor=BG_CARD,
            column_spacing=35,
            divider_thickness=1,
            expand=True
        )

        # --- GRID FINAL ---
        area_dashboard = self.ft.Column([
            header,
            self.ft.Container(height=10),
            painel_dados_consolidados,
            self.ft.Container(height=10),
            top_section,
            self.ft.Container(height=10),
            status_row,
            self.ft.Container(height=10),
            charts_row_1,
            self.ft.Container(height=15),
            charts_row_2,
            self.ft.Container(height=15),
            self.ft.Text("Registros de Telemetria Recentes", size=16, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            self.ft.Container(height=5),
            self.ft.Container(
                bgcolor=BG_CARD,
                padding=10,
                border_radius=10,
                border=self.ft.border.all(1, BORDER_COLOR),
                content=self.ft.Row([readings_table], scroll=self.ft.ScrollMode.ALWAYS)
            )
        ], expand=True, scroll=self.ft.ScrollMode.AUTO)

        self.mostrar_popup_pareamento()
        return area_dashboard